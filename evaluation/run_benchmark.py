#!/usr/bin/env python3
"""Run and objectively score the frozen InfraGuard AI benchmark.

The harness reuses the repository's production prompt assembly, verdict parser,
runbook loader, local embedding adapter, and top-four similarity search. It
retains every raw response and resumes safely from JSONL checkpoints.

Qualitative root-cause, action, and grounding scores are intentionally left
blank for independent human assessors. The script never substitutes an LLM
judge for the practitioner scoring required by the protocol.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import statistics
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


EVALUATION_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVALUATION_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent.llm.prompts import assemble_prompt_from_collected  # noqa: E402
from agent.llm.schema import VERDICT_SYSTEM_INSTRUCTION, parse_verdict_text  # noqa: E402
from agent.rag.local_runbooks_loader import load_local_runbooks  # noqa: E402
from agent.rag.vector_store import build_index, similarity_search  # noqa: E402


SEVERITIES = ["ok", "warning", "high", "critical"]
SIGNATURE_RE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_.-]+:.+$")
RAG_SYSTEM = (
    "You are an on-call assistant for infrastructure operations. "
    "Answer the question based ONLY on the runbooks provided below. "
    "If the runbooks do not contain relevant information, say so clearly. "
    "Be concise and actionable."
)
NO_RAG_SYSTEM = (
    "You are an on-call assistant for infrastructure operations. "
    "No local runbook context is available. Answer using only your existing knowledge, "
    "be explicit about uncertainty, and be concise and actionable."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def source_snapshot() -> dict[str, Any]:
    fixed = [
        "agent/llm/prompts.py",
        "agent/llm/schema.py",
        "agent/rag/local_runbooks_loader.py",
        "agent/rag/vector_store.py",
        "evaluation/benchmark_v1.json",
        "evaluation/run_benchmark.py",
    ]
    paths = [REPO_ROOT / relative for relative in fixed]
    paths.extend(sorted((REPO_ROOT / "runbooks").rglob("*.md")))
    entries: list[dict[str, Any]] = []
    combined = hashlib.sha256()
    for path in paths:
        relative = path.relative_to(REPO_ROOT).as_posix()
        data = path.read_bytes()
        digest = sha256_bytes(data)
        entries.append({"path": relative, "sha256": digest, "bytes": len(data)})
        combined.update(relative.encode("utf-8"))
        combined.update(b"\0")
        combined.update(data)
        combined.update(b"\0")
    return {
        "combined_sha256": combined.hexdigest(),
        "file_count": len(entries),
        "files": entries,
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return rows


def validate_existing_rows(
    rows: list[dict[str, Any]], *, spec_hash: str, model: str, temperature: float
) -> None:
    for row in rows:
        if row.get("spec_sha256") != spec_hash:
            raise ValueError("Existing result rows use a different frozen benchmark specification")
        if row.get("model") != model:
            raise ValueError("Existing result rows use a different model")
        if float(row.get("temperature")) != float(temperature):
            raise ValueError("Existing result rows use a different temperature")


def http_json(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=20) as response:  # noqa: S310 - controlled local endpoint
        return json.loads(response.read().decode("utf-8"))


def model_metadata(base_url: str, model: str) -> dict[str, Any]:
    root = base_url.removesuffix("/v1").rstrip("/")
    metadata: dict[str, Any] = {"requested_model": model, "base_url_kind": "local_ollama"}
    try:
        metadata["ollama_version"] = http_json(f"{root}/api/version").get("version")
    except Exception as exc:  # noqa: BLE001
        metadata["version_error"] = str(exc)
    try:
        tags = http_json(f"{root}/api/tags").get("models", [])
        match = next((item for item in tags if item.get("name") == model or item.get("model") == model), None)
        if match:
            metadata.update(
                {
                    "resolved_model": match.get("model") or match.get("name"),
                    "digest": match.get("digest"),
                    "size_bytes": match.get("size"),
                    "details": match.get("details"),
                    "modified_at": match.get("modified_at"),
                }
            )
    except Exception as exc:  # noqa: BLE001
        metadata["tags_error"] = str(exc)
    return metadata


def openai_client(base_url: str):
    from openai import OpenAI

    return OpenAI(base_url=base_url.rstrip("/"), api_key="ollama", timeout=300.0, max_retries=0)


def call_model(
    client: Any,
    *,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        elapsed = time.perf_counter() - started
        choice = response.choices[0] if response.choices else None
        raw = (choice.message.content or "") if choice else ""
        usage = response.usage
        return {
            "ok": True,
            "raw_output": raw,
            "latency_seconds": round(elapsed, 6),
            "prompt_tokens": getattr(usage, "prompt_tokens", None) if usage else None,
            "completion_tokens": getattr(usage, "completion_tokens", None) if usage else None,
            "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
            "finish_reason": getattr(choice, "finish_reason", None) if choice else None,
            "response_model": getattr(response, "model", None),
            "response_id": getattr(response, "id", None),
        }
    except Exception as exc:  # noqa: BLE001
        elapsed = time.perf_counter() - started
        return {
            "ok": False,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "latency_seconds": round(elapsed, 6),
        }


def run_incidents(
    spec: dict[str, Any],
    spec_hash: str,
    output_dir: Path,
    client: Any,
    model: str,
    model_info: dict[str, Any],
    runs: int,
    temperature: float,
) -> None:
    path = output_dir / "incident_runs.jsonl"
    existing_rows = read_jsonl(path)
    validate_existing_rows(existing_rows, spec_hash=spec_hash, model=model, temperature=temperature)
    existing = {(row.get("scenario_id"), row.get("repeat")) for row in existing_rows}
    scenarios = spec["incident_scenarios"]
    total = len(scenarios) * runs
    completed = len(existing)
    for scenario in scenarios:
        prompt = assemble_prompt_from_collected(
            scenario["collected"], known_conditions=scenario.get("known_conditions")
        ).strip()
        for repeat in range(1, runs + 1):
            key = (scenario["id"], repeat)
            if key in existing:
                continue
            result = call_model(
                client,
                model=model,
                messages=[
                    {"role": "system", "content": VERDICT_SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=320,
            )
            parsed = parse_verdict_text(result.get("raw_output", "")) if result.get("ok") else {
                "ok": False,
                "error": result.get("error_type", "request_failed"),
                "message": result.get("error_message", "request failed"),
            }
            row = {
                "kind": "incident",
                "benchmark_version": spec["benchmark_version"],
                "spec_sha256": spec_hash,
                "prompt_version": spec["prompt_version"],
                "scenario_id": scenario["id"],
                "category": scenario["category"],
                "gold_severity": scenario["gold_severity"],
                "repeat": repeat,
                "timestamp_utc": utc_now(),
                "model": model,
                "model_digest": model_info.get("digest"),
                "temperature": temperature,
                "prompt_sha256": sha256_text(VERDICT_SYSTEM_INSTRUCTION + "\n" + prompt),
                "prompt": prompt,
                "request_result": result,
                "parsed": parsed,
                "metered_api_cost_usd": 0.0,
                "cost_note": "Local Ollama execution; excludes electricity and hardware depreciation.",
            }
            append_jsonl(path, row)
            completed += 1
            status = parsed.get("severity") if parsed.get("ok") else parsed.get("error")
            print(
                f"incident {completed}/{total} {scenario['id']} repeat={repeat} "
                f"status={status} latency={result.get('latency_seconds')}s",
                flush=True,
            )


def format_runbook_context(documents: Iterable[Any]) -> str:
    parts: list[str] = []
    for index, document in enumerate(documents, start=1):
        title = document.metadata.get("title", "Untitled")
        source = document.metadata.get("source", "")
        parts.append(
            f"--- Runbook {index}: {title} ({source}) ---\n{document.page_content}"
        )
    return "\n\n".join(parts) if parts else "No runbooks found."


def normalise_source(source: str) -> str:
    return source.removeprefix("file://").replace("\\", "/")


def build_retrieval_record(spec: dict[str, Any]) -> dict[str, Any]:
    documents = load_local_runbooks()
    indexed = build_index(documents)
    if indexed != len(documents) or indexed == 0:
        raise RuntimeError(f"Runbook indexing failed: loaded={len(documents)} indexed={indexed}")
    questions: list[dict[str, Any]] = []
    for question in spec["rag_questions"]:
        docs = similarity_search(question["question"], k=4)
        sources = [normalise_source(str(doc.metadata.get("source", ""))) for doc in docs]
        questions.append(
            {
                "id": question["id"],
                "question": question["question"],
                "relevant_runbook": question["relevant_runbook"],
                "retrieved_sources": sources,
                "retrieved_titles": [str(doc.metadata.get("title", "Untitled")) for doc in docs],
                "retrieval_success": question["relevant_runbook"] in sources,
                "context": format_runbook_context(docs),
            }
        )
    return {
        "timestamp_utc": utc_now(),
        "runbook_count": len(documents),
        "indexed_count": indexed,
        "retrieval_depth": 4,
        "questions": questions,
    }


def write_retrieval(spec: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    record = build_retrieval_record(spec)
    path = output_dir / "retrieval.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    successes = sum(1 for row in record["questions"] if row["retrieval_success"])
    print(f"retrieval {successes}/{len(record['questions'])} labelled runbooks found in top four", flush=True)
    return record


def run_rag(
    spec: dict[str, Any],
    spec_hash: str,
    output_dir: Path,
    client: Any,
    model: str,
    model_info: dict[str, Any],
    runs: int,
    temperature: float,
) -> None:
    retrieval = write_retrieval(spec, output_dir)
    path = output_dir / "rag_runs.jsonl"
    existing_rows = read_jsonl(path)
    validate_existing_rows(existing_rows, spec_hash=spec_hash, model=model, temperature=temperature)
    existing = {
        (row.get("question_id"), row.get("condition"), row.get("repeat"))
        for row in existing_rows
    }
    by_id = {item["id"]: item for item in retrieval["questions"]}
    total = len(spec["rag_questions"]) * 2 * runs
    completed = len(existing)
    for question in spec["rag_questions"]:
        retrieval_row = by_id[question["id"]]
        for condition in ("rag", "no_rag"):
            if condition == "rag":
                system = RAG_SYSTEM
                user = (
                    f"RUNBOOK CONTEXT:\n{retrieval_row['context']}\n\n"
                    f"QUESTION: {question['question']}"
                )
            else:
                system = NO_RAG_SYSTEM
                user = f"QUESTION: {question['question']}"
            for repeat in range(1, runs + 1):
                key = (question["id"], condition, repeat)
                if key in existing:
                    continue
                result = call_model(
                    client,
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    max_tokens=420,
                )
                row = {
                    "kind": "rag",
                    "benchmark_version": spec["benchmark_version"],
                    "spec_sha256": spec_hash,
                    "question_id": question["id"],
                    "repeat": repeat,
                    "condition": condition,
                    "timestamp_utc": utc_now(),
                    "model": model,
                    "model_digest": model_info.get("digest"),
                    "temperature": temperature,
                    "prompt_sha256": sha256_text(system + "\n" + user),
                    "question": question["question"],
                    "relevant_runbook": question["relevant_runbook"],
                    "retrieved_sources": retrieval_row["retrieved_sources"] if condition == "rag" else [],
                    "retrieval_success": retrieval_row["retrieval_success"] if condition == "rag" else None,
                    "system_prompt": system,
                    "user_prompt": user,
                    "request_result": result,
                    "metered_api_cost_usd": 0.0,
                    "cost_note": "Local Ollama execution; excludes electricity and hardware depreciation.",
                }
                append_jsonl(path, row)
                completed += 1
                status = "ok" if result.get("ok") else result.get("error_type")
                print(
                    f"rag {completed}/{total} {question['id']} condition={condition} repeat={repeat} "
                    f"status={status} latency={result.get('latency_seconds')}s",
                    flush=True,
                )


def percentile(values: list[float], percentile_value: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(percentile_value * len(ordered)) - 1))
    return round(ordered[index], 6)


def mean_or_none(values: list[float | int | None]) -> float | None:
    clean = [float(value) for value in values if value is not None]
    return round(statistics.mean(clean), 6) if clean else None


def classification_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    confusion = {gold: {pred: 0 for pred in SEVERITIES + ["invalid"]} for gold in SEVERITIES}
    for row in rows:
        gold = row["gold_severity"]
        parsed = row.get("parsed") or {}
        predicted = parsed.get("severity") if parsed.get("ok") else "invalid"
        confusion[gold][predicted] += 1

    per_class: dict[str, Any] = {}
    for label in SEVERITIES:
        tp = confusion[label][label]
        fp = sum(confusion[gold][label] for gold in SEVERITIES if gold != label)
        fn = sum(confusion[label][pred] for pred in SEVERITIES + ["invalid"] if pred != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[label] = {
            "precision": round(precision, 6),
            "recall": round(recall, 6),
            "f1": round(f1, 6),
            "support": sum(confusion[label].values()),
        }
    return {
        "confusion_matrix": confusion,
        "per_class": per_class,
        "macro_precision": round(statistics.mean(item["precision"] for item in per_class.values()), 6),
        "macro_recall": round(statistics.mean(item["recall"] for item in per_class.values()), 6),
        "macro_f1": round(statistics.mean(item["f1"] for item in per_class.values()), 6),
    }


def objective_incident_summary(rows: list[dict[str, Any]], spec: dict[str, Any]) -> dict[str, Any]:
    scenario_by_id = {row["id"]: row for row in spec["incident_scenarios"]}
    signature_groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        parsed = row.get("parsed") or {}
        if parsed.get("ok"):
            signature_groups[row["scenario_id"]].append(str(parsed.get("signature", "")))
    stable_by_scenario = {
        scenario_id: len(values) == spec["runs_per_case"] and len(set(values)) == 1
        for scenario_id, values in signature_groups.items()
    }

    for row in rows:
        parsed = row.get("parsed") or {}
        schema_valid = bool(parsed.get("ok"))
        signature = str(parsed.get("signature", "")) if schema_valid else ""
        expected = scenario_by_id[row["scenario_id"]].get("expected_signature")
        row["objective_scores"] = {
            "schema_valid": schema_valid,
            "severity_exact": schema_valid and parsed.get("severity") == row["gold_severity"],
            "signature_format": bool(SIGNATURE_RE.match(signature)),
            "signature_stable_across_repeats": stable_by_scenario.get(row["scenario_id"], False),
            "expected_signature_exact": (signature == expected) if expected else None,
        }

    total = len(rows)
    valid = sum(1 for row in rows if row["objective_scores"]["schema_valid"])
    exact = sum(1 for row in rows if row["objective_scores"]["severity_exact"])
    signature_format = sum(1 for row in rows if row["objective_scores"]["signature_format"])
    expected_rows = [row for row in rows if row["objective_scores"]["expected_signature_exact"] is not None]
    expected_passes = sum(1 for row in expected_rows if row["objective_scores"]["expected_signature_exact"])
    stable_count = sum(1 for passed in stable_by_scenario.values() if passed)
    false_positives = sum(
        1
        for row in rows
        if row["gold_severity"] == "ok"
        and (row.get("parsed") or {}).get("ok")
        and (row.get("parsed") or {}).get("severity") in {"warning", "high", "critical"}
    )
    false_negatives = sum(
        1
        for row in rows
        if row["gold_severity"] in {"high", "critical"}
        and (row.get("parsed") or {}).get("ok")
        and (row.get("parsed") or {}).get("severity") in {"ok", "warning"}
    )
    latencies = [float(row["request_result"]["latency_seconds"]) for row in rows]
    classification = classification_metrics(rows)
    return {
        "run_count": total,
        "scenario_count": len(scenario_by_id),
        "schema_valid_count": valid,
        "schema_valid_rate": round(valid / total, 6) if total else None,
        "severity_exact_count": exact,
        "severity_accuracy": round(exact / total, 6) if total else None,
        "false_positive_count": false_positives,
        "false_negative_count": false_negatives,
        "signature_format_rate": round(signature_format / total, 6) if total else None,
        "signature_stable_scenario_count": stable_count,
        "signature_stability_rate": round(stable_count / len(scenario_by_id), 6) if scenario_by_id else None,
        "expected_signature_exact_count": expected_passes,
        "expected_signature_exact_rate": round(expected_passes / len(expected_rows), 6) if expected_rows else None,
        "p50_latency_seconds": percentile(latencies, 0.50),
        "p95_latency_seconds": percentile(latencies, 0.95),
        "mean_latency_seconds": mean_or_none(latencies),
        "mean_prompt_tokens": mean_or_none([row["request_result"].get("prompt_tokens") for row in rows]),
        "mean_completion_tokens": mean_or_none([row["request_result"].get("completion_tokens") for row in rows]),
        "metered_api_cost_usd": 0.0,
        "cost_boundary": "Local Ollama has no metered provider charge; energy and hardware cost were not measured.",
        **classification,
        "qualitative_scoring_status": "Pending two independent human assessors.",
    }


def objective_rag_summary(rows: list[dict[str, Any]], retrieval: dict[str, Any]) -> dict[str, Any]:
    successful_requests = [row for row in rows if row.get("request_result", {}).get("ok")]
    by_condition: dict[str, Any] = {}
    for condition in ("rag", "no_rag"):
        condition_rows = [row for row in rows if row["condition"] == condition]
        latencies = [float(row["request_result"]["latency_seconds"]) for row in condition_rows]
        by_condition[condition] = {
            "run_count": len(condition_rows),
            "successful_request_count": sum(1 for row in condition_rows if row["request_result"].get("ok")),
            "p50_latency_seconds": percentile(latencies, 0.50),
            "p95_latency_seconds": percentile(latencies, 0.95),
            "mean_latency_seconds": mean_or_none(latencies),
            "mean_prompt_tokens": mean_or_none([row["request_result"].get("prompt_tokens") for row in condition_rows]),
            "mean_completion_tokens": mean_or_none([row["request_result"].get("completion_tokens") for row in condition_rows]),
        }
    retrieval_successes = sum(1 for row in retrieval["questions"] if row["retrieval_success"])
    return {
        "run_count": len(rows),
        "successful_request_count": len(successful_requests),
        "question_count": len(retrieval["questions"]),
        "retrieval_success_count": retrieval_successes,
        "retrieval_success_rate": round(retrieval_successes / len(retrieval["questions"]), 6),
        "retrieval_depth": retrieval["retrieval_depth"],
        "by_condition": by_condition,
        "metered_api_cost_usd": 0.0,
        "cost_boundary": "Local Ollama has no metered provider charge; energy and hardware cost were not measured.",
        "qualitative_comparison_status": "RAG/no-RAG answer correctness and grounding await independent human scoring.",
    }


def assessment_id(*parts: Any) -> str:
    return sha256_text("|".join(str(part) for part in parts))[:12].upper()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_assessor_files(
    output_dir: Path,
    incident_rows: list[dict[str, Any]],
    rag_rows: list[dict[str, Any]],
    spec: dict[str, Any],
) -> None:
    scenario_by_id = {row["id"]: row for row in spec["incident_scenarios"]}
    incident_worksheet: list[dict[str, Any]] = []
    incident_key: list[dict[str, Any]] = []
    for row in incident_rows:
        scenario = scenario_by_id[row["scenario_id"]]
        parsed = row.get("parsed") or {}
        aid = assessment_id("incident", row["scenario_id"], row["repeat"], spec["benchmark_version"])
        incident_worksheet.append(
            {
                "assessment_id": aid,
                "controlled_evidence": scenario["controlled_evidence"],
                "returned_severity": parsed.get("severity", "<parse failure>"),
                "returned_summary": parsed.get("summary", ""),
                "returned_root_cause": parsed.get("root_cause", ""),
                "returned_action": parsed.get("recommended_action", ""),
                "returned_signature": parsed.get("signature", ""),
                "root_cause_score_0_2": "",
                "action_score_0_2": "",
                "grounding_score_0_2": "",
                "assessor_notes": "",
            }
        )
        incident_key.append(
            {
                "assessment_id": aid,
                "scenario_id": row["scenario_id"],
                "repeat": row["repeat"],
                "gold_severity": scenario["gold_severity"],
                "root_cause_reference": scenario["root_cause_reference"],
                "action_reference": scenario["action_reference"],
            }
        )
    incident_fields = [
        "assessment_id",
        "controlled_evidence",
        "returned_severity",
        "returned_summary",
        "returned_root_cause",
        "returned_action",
        "returned_signature",
        "root_cause_score_0_2",
        "action_score_0_2",
        "grounding_score_0_2",
        "assessor_notes",
    ]
    write_csv(output_dir / "assessor_incident_worksheet_A.csv", incident_fields, incident_worksheet)
    write_csv(output_dir / "assessor_incident_worksheet_B.csv", incident_fields, incident_worksheet)
    write_csv(
        output_dir / "assessor_incident_key.csv",
        ["assessment_id", "scenario_id", "repeat", "gold_severity", "root_cause_reference", "action_reference"],
        incident_key,
    )

    rag_worksheet: list[dict[str, Any]] = []
    rag_key: list[dict[str, Any]] = []
    for row in rag_rows:
        aid = assessment_id("rag", row["question_id"], row["condition"], row["repeat"], spec["benchmark_version"])
        rag_worksheet.append(
            {
                "assessment_id": aid,
                "question": row["question"],
                "provided_sources": "; ".join(row.get("retrieved_sources") or []),
                "answer": row.get("request_result", {}).get("raw_output", ""),
                "correctness_score_0_2": "",
                "grounding_score_0_2": "",
                "assessor_notes": "",
            }
        )
        rag_key.append(
            {
                "assessment_id": aid,
                "question_id": row["question_id"],
                "condition": row["condition"],
                "repeat": row["repeat"],
                "frozen_relevant_runbook": row["relevant_runbook"],
            }
        )
    rag_fields = [
        "assessment_id",
        "question",
        "provided_sources",
        "answer",
        "correctness_score_0_2",
        "grounding_score_0_2",
        "assessor_notes",
    ]
    write_csv(output_dir / "assessor_rag_worksheet_A.csv", rag_fields, rag_worksheet)
    write_csv(output_dir / "assessor_rag_worksheet_B.csv", rag_fields, rag_worksheet)
    write_csv(
        output_dir / "assessor_rag_key.csv",
        ["assessment_id", "question_id", "condition", "repeat", "frozen_relevant_runbook"],
        rag_key,
    )


def format_percent(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def write_report(path: Path, summary: dict[str, Any]) -> None:
    incident = summary.get("incident")
    rag = summary.get("rag")
    lines = [
        "# InfraGuard AI Controlled Benchmark - Objective Results",
        "",
        f"- Benchmark version: {summary['benchmark_version']}",
        f"- Specification SHA-256: `{summary['spec_sha256']}`",
        f"- Model: `{summary['model_metadata'].get('resolved_model') or summary['model_metadata'].get('requested_model')}`",
        f"- Model digest: `{summary['model_metadata'].get('digest') or 'unavailable'}`",
        f"- Ollama version: `{summary['model_metadata'].get('ollama_version') or 'unavailable'}`",
        f"- Temperature: {summary['temperature']}",
        f"- Generated: {summary['generated_at_utc']}",
        "",
        "## Evidence boundary",
        "",
        "These are objective automated measurements from a local-model run. Root-cause, recommended-action, evidence-grounding, and RAG answer-quality scores remain blank until two independent human assessors complete the supplied worksheets. The run does not establish results for Gemini, Anthropic, OpenAI-compatible cloud models, or DeepSeek. Local Ollama has no metered API charge; electricity and hardware cost were not measured.",
        "",
    ]
    if incident:
        lines.extend(
            [
                "## Incident benchmark",
                "",
                f"- Runs: {incident['run_count']} across {incident['scenario_count']} scenarios",
                f"- Schema-valid output rate: {format_percent(incident['schema_valid_rate'])}",
                f"- Exact severity accuracy: {format_percent(incident['severity_accuracy'])}",
                f"- Macro F1: {incident['macro_f1']:.3f}",
                f"- False positives: {incident['false_positive_count']}",
                f"- False negatives: {incident['false_negative_count']}",
                f"- Signature-format pass rate: {format_percent(incident['signature_format_rate'])}",
                f"- Signature-stability rate by scenario: {format_percent(incident['signature_stability_rate'])}",
                f"- Expected-signature exact rate: {format_percent(incident['expected_signature_exact_rate'])}",
                f"- Latency p50 / p95: {incident['p50_latency_seconds']} s / {incident['p95_latency_seconds']} s",
                f"- Mean input / output tokens: {incident['mean_prompt_tokens']} / {incident['mean_completion_tokens']}",
                "",
            ]
        )
    if rag:
        lines.extend(
            [
                "## RAG benchmark",
                "",
                f"- Generation runs: {rag['run_count']} ({rag['successful_request_count']} successful)",
                f"- Labelled retrieval success at top four: {rag['retrieval_success_count']}/{rag['question_count']} ({format_percent(rag['retrieval_success_rate'])})",
                f"- RAG latency p50 / p95: {rag['by_condition']['rag']['p50_latency_seconds']} s / {rag['by_condition']['rag']['p95_latency_seconds']} s",
                f"- No-RAG latency p50 / p95: {rag['by_condition']['no_rag']['p50_latency_seconds']} s / {rag['by_condition']['no_rag']['p95_latency_seconds']} s",
                "- Comparative answer correctness and grounding: pending independent human scoring",
                "",
            ]
        )
    lines.extend(
        [
            "## Retained evidence",
            "",
            "- `incident_runs.jsonl`: prompts, raw outputs, parsed outputs, timings, and token counts.",
            "- `rag_runs.jsonl`: RAG/no-RAG prompts, raw answers, sources, timings, and token counts.",
            "- `retrieval.json`: frozen top-four retrieval results.",
            "- `assessor_*_worksheet_A.csv` and `assessor_*_worksheet_B.csv`: separate blinded scoring sheets.",
            "- `assessor_*_key.csv`: held-back answer keys for reconciliation after initial scoring.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def score_results(
    spec: dict[str, Any],
    spec_hash: str,
    output_dir: Path,
    model_info: dict[str, Any],
    temperature: float,
) -> dict[str, Any]:
    incident_rows = read_jsonl(output_dir / "incident_runs.jsonl")
    rag_rows = read_jsonl(output_dir / "rag_runs.jsonl")
    retrieval_path = output_dir / "retrieval.json"
    retrieval = load_json(retrieval_path) if retrieval_path.exists() else None
    summary: dict[str, Any] = {
        "benchmark_version": spec["benchmark_version"],
        "spec_sha256": spec_hash,
        "generated_at_utc": utc_now(),
        "temperature": temperature,
        "model_metadata": model_info,
        "evidence_boundary": {
            "automated_objective_metrics_only": True,
            "independent_human_incident_scores_complete": False,
            "independent_human_rag_scores_complete": False,
            "practitioner_usability_study_complete": False,
        },
    }
    if incident_rows:
        summary["incident"] = objective_incident_summary(incident_rows, spec)
        # Persist the objective scores without rewriting the append-only raw JSONL.
        write_csv(
            output_dir / "incident_objective_scores.csv",
            [
                "scenario_id",
                "category",
                "repeat",
                "gold_severity",
                "predicted_severity",
                "schema_valid",
                "severity_exact",
                "signature_format",
                "signature_stable_across_repeats",
                "expected_signature_exact",
                "latency_seconds",
                "prompt_tokens",
                "completion_tokens",
            ],
            (
                {
                    "scenario_id": row["scenario_id"],
                    "category": row["category"],
                    "repeat": row["repeat"],
                    "gold_severity": row["gold_severity"],
                    "predicted_severity": (row.get("parsed") or {}).get("severity", "invalid"),
                    **row["objective_scores"],
                    "latency_seconds": row["request_result"].get("latency_seconds"),
                    "prompt_tokens": row["request_result"].get("prompt_tokens"),
                    "completion_tokens": row["request_result"].get("completion_tokens"),
                }
                for row in incident_rows
            ),
        )
    if rag_rows and retrieval:
        summary["rag"] = objective_rag_summary(rag_rows, retrieval)
    if incident_rows or rag_rows:
        write_assessor_files(output_dir, incident_rows, rag_rows, spec)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_report(output_dir / "report.md", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--spec", type=Path, default=EVALUATION_DIR / "benchmark_v1.json", help="Frozen benchmark JSON"
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="qwen2.5:3b")
    parser.add_argument("--base-url", default="http://ollama:11434/v1")
    parser.add_argument("--runs", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument(
        "--phase", choices=("retrieval", "incident", "rag", "all", "score"), default="all"
    )
    args = parser.parse_args()

    spec_bytes = args.spec.read_bytes()
    spec = json.loads(spec_bytes)
    spec_hash = sha256_bytes(spec_bytes)
    runs = args.runs if args.runs is not None else int(spec["runs_per_case"])
    temperature = args.temperature if args.temperature is not None else float(spec["temperature"])
    if runs != int(spec["runs_per_case"]):
        raise SystemExit(
            f"Refusing non-protocol repeat count: spec requires {spec['runs_per_case']}, got {runs}"
        )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    os.environ["RUNBOOKS_DIR"] = str(REPO_ROOT / "runbooks")

    model_info = model_metadata(args.base_url, args.model)
    manifest = {
        "benchmark_version": spec["benchmark_version"],
        "spec_sha256": spec_hash,
        "spec_path": str(args.spec),
        "started_or_resumed_at_utc": utc_now(),
        "runs_per_case": runs,
        "temperature": temperature,
        "model_metadata": model_info,
        "source_snapshot": source_snapshot(),
        "python_version": sys.version,
        "production_modules_reused": [
            "agent.llm.prompts.assemble_prompt_from_collected",
            "agent.llm.schema.VERDICT_SYSTEM_INSTRUCTION",
            "agent.llm.schema.parse_verdict_text",
            "agent.rag.local_runbooks_loader.load_local_runbooks",
            "agent.rag.vector_store.build_index",
            "agent.rag.vector_store.similarity_search",
        ],
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if args.phase == "retrieval":
        write_retrieval(spec, args.output_dir)
        return

    client = None
    if args.phase in {"incident", "rag", "all"}:
        client = openai_client(args.base_url)
    if args.phase in {"incident", "all"}:
        run_incidents(spec, spec_hash, args.output_dir, client, args.model, model_info, runs, temperature)
    if args.phase in {"rag", "all"}:
        run_rag(spec, spec_hash, args.output_dir, client, args.model, model_info, runs, temperature)
    if args.phase in {"incident", "rag", "all", "score"}:
        summary = score_results(spec, spec_hash, args.output_dir, model_info, temperature)
        incident = summary.get("incident", {})
        rag = summary.get("rag", {})
        if incident:
            print(
                "incident summary: "
                f"severity_accuracy={incident.get('severity_accuracy')} "
                f"schema_valid_rate={incident.get('schema_valid_rate')} "
                f"macro_f1={incident.get('macro_f1')}",
                flush=True,
            )
        if rag:
            print(
                "rag summary: "
                f"retrieval_success_rate={rag.get('retrieval_success_rate')} "
                f"successful_requests={rag.get('successful_request_count')}/{rag.get('run_count')}",
                flush=True,
            )


if __name__ == "__main__":
    main()

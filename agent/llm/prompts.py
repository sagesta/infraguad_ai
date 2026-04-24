"""Prompt assembly for Vertex AI (Gemini) SRE verdicts."""

from __future__ import annotations

import json
from typing import Any


def _include_http_probe_block(collected: dict[str, Any]) -> bool:
    if "http_probe" not in collected:
        return False
    probe = collected["http_probe"]
    if not isinstance(probe, dict):
        return True
    return not (probe.get("ok") is False and probe.get("error") == "missing_env")


def _include_docker_logs_block(collected: dict[str, Any]) -> bool:
    logs = collected.get("docker_logs")
    return isinstance(logs, list) and len(logs) > 0


def assemble_prompt_from_collected(collected: dict[str, Any]) -> str:
    """Serialize tool outputs into telemetry blocks for Gemini.

    Loki and Prometheus sections appear only when present in ``collected``.
    HTTP probe is skipped when absent or when the payload is only a PROBE_URLS
    ``missing_env`` sentinel. Docker log errors appear only when the list is non-empty.
    """
    blocks: list[str] = []

    if "loki" in collected:
        blocks.append(
            "=== LOGS (last 50 lines) ===\n" + json.dumps(collected["loki"], indent=2, default=str)
        )
    if "prometheus" in collected:
        blocks.append(
            "=== METRICS (CPU/RAM/Disk) ===\n"
            + json.dumps(collected["prometheus"], indent=2, default=str)
        )

    blocks.append(
        "=== DOCKER EVENTS (last 60s) ===\n" + json.dumps(collected.get("docker"), indent=2, default=str)
    )
    if _include_http_probe_block(collected):
        blocks.append(
            "=== HTTP PROBE RESULTS ===\n" + json.dumps(collected["http_probe"], indent=2, default=str)
        )
    if _include_docker_logs_block(collected):
        blocks.append(
            "=== DEVPLANNER DOCKER LOG ERRORS (keyword-filtered tail) ===\n"
            + json.dumps(collected["docker_logs"], indent=2, default=str)
        )

    telemetry = "\n\n".join(blocks)

    return f"""
You are a senior SRE analyzing infrastructure telemetry.
Only the telemetry sections below are in scope. Any standard integration (logs, metrics, HTTP probes) not shown was intentionally omitted because it is not configured for this deployment — treat that as normal, not as missing infrastructure or an incident. Judge severity only from the JSON blocks present.

Return ONLY valid JSON with these fields:
- severity: one of "ok", "warning", "high", "critical"
- summary: one sentence describing current state
- root_cause: detailed analysis of what is wrong and why
- recommended_action: specific steps to resolve

TELEMETRY DATA:

{telemetry}
"""

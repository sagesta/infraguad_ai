"""LangGraph orchestration for collect → analyze → decide → notify."""

from __future__ import annotations

import json
import os
from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from agent.llm.prompts import assemble_prompt_from_collected
from agent.llm.vertex import get_verdict
from agent.tools.docker_events import get_docker_events
from agent.tools.http_probe import probe_endpoints
from agent.tools.loki import fetch_loki_logs
from agent.tools.notify import send_push_notification
from agent.tools.prometheus import query_prometheus
from agent.tools.docker_api import collect_container_diagnostics


def _env_url_set(name: str) -> bool:
    return bool(os.environ.get(name, "").strip())


class GraphState(TypedDict, total=False):
    """``docker_log_errors`` is optional seed data from ``main`` heartbeat (Docker log scan)."""

    docker_log_errors: list[dict[str, str]]
    collected: dict[str, Any]
    verdict: dict[str, Any]
    raw_llm: str
    llm_error: str | None
    docker_context: dict[str, Any] | None
    notify_result: dict[str, Any] | None


def _collect_data(state: GraphState) -> dict[str, Any]:
    docker_logs = state.get("docker_log_errors")
    if docker_logs is None:
        docker_logs = []

    collected: dict[str, Any] = {
        "docker": get_docker_events(),
        "docker_logs": docker_logs,
    }
    if _env_url_set("PROBE_URLS"):
        collected["http_probe"] = probe_endpoints()
    if _env_url_set("LOKI_URL"):
        collected["loki"] = fetch_loki_logs()
    if _env_url_set("PROMETHEUS_URL"):
        collected["prometheus"] = query_prometheus()
    # Never pass loki/prometheus in ``collected`` when URLs are unset (no key, not None).
    if not _env_url_set("LOKI_URL"):
        collected.pop("loki", None)
    if not _env_url_set("PROMETHEUS_URL"):
        collected.pop("prometheus", None)
    return {"collected": collected}


def _fallback_verdict(message: str) -> dict[str, Any]:
    return {
        "severity": "warning",
        "summary": "Analysis pipeline degraded; operator review required.",
        "root_cause": message,
        "recommended_action": "Verify Vertex AI / GCP credentials, quotas, and network egress.",
    }


def _analyze(state: GraphState) -> dict[str, Any]:
    collected = state.get("collected") or {}
    prompt = assemble_prompt_from_collected(collected)
    llm = get_verdict(prompt)
    if not llm.get("ok"):
        verdict = _fallback_verdict(str(llm.get("message", llm.get("error", "unknown_error"))))
        return {
            "raw_llm": "",
            "llm_error": str(llm.get("message", llm.get("error"))),
            "verdict": verdict,
        }

    raw_llm = str(llm.get("_raw_text", ""))
    verdict = {
        "severity": str(llm.get("severity", "warning")),
        "summary": str(llm.get("summary", "")),
        "root_cause": str(llm.get("root_cause", "")),
        "recommended_action": str(llm.get("recommended_action", "")),
    }

    return {
        "raw_llm": raw_llm,
        "llm_error": None,
        "verdict": verdict,
    }


def _decide_action(state: GraphState) -> dict[str, Any]:
    verdict = state.get("verdict") or {}
    if verdict.get("severity") == "critical":
        diag = collect_container_diagnostics()
        merged = dict(verdict)
        if diag.get("ok"):
            merged["root_cause"] = merged.get("root_cause", "") + "\n\nDocker context:\n" + json.dumps(
                diag, indent=2, default=str
            )
        else:
            merged["root_cause"] = merged.get("root_cause", "") + "\n\nDocker diagnostics failed:\n" + json.dumps(
                diag, indent=2, default=str
            )
        return {"docker_context": diag, "verdict": merged}
    return {"docker_context": None}


def _route_notify(state: GraphState) -> Literal["notify", "skip"]:
    verdict = state.get("verdict") or {}
    sev = str(verdict.get("severity", "ok")).lower()
    if sev in {"high", "critical"}:
        return "notify"
    return "skip"


def _notify(state: GraphState) -> dict[str, Any]:
    verdict = state.get("verdict") or {}
    sev = str(verdict.get("severity", "ok")).lower()
    title = f"InfraGuard alert [{sev}]"
    body_parts = [
        str(verdict.get("summary", "")),
        "",
        str(verdict.get("recommended_action", "")),
    ]
    message = "\n".join(body_parts).strip()
    result = send_push_notification(title=title, message=message, severity=sev)
    return {"notify_result": result}


def build_graph() -> Any:
    graph = StateGraph(GraphState)
    graph.add_node("collect_data", _collect_data)
    graph.add_node("analyze", _analyze)
    graph.add_node("decide_action", _decide_action)
    graph.add_node("notify", _notify)

    graph.add_edge(START, "collect_data")
    graph.add_edge("collect_data", "analyze")
    graph.add_edge("analyze", "decide_action")
    graph.add_conditional_edges(
        "decide_action",
        _route_notify,
        {
            "notify": "notify",
            "skip": END,
        },
    )
    graph.add_edge("notify", END)
    return graph.compile()


def run_cycle(initial: GraphState | None = None) -> GraphState:
    """Execute one full orchestration cycle synchronously.

    Pass ``initial`` with ``docker_log_errors`` (from ``main`` heartbeat) so Gemini sees
    DevPlanner container error lines without calling Docker from the LangGraph thread.
    """
    app = build_graph()
    result: GraphState = app.invoke(dict(initial) if initial else {})
    return result

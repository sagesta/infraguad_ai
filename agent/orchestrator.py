"""LangGraph orchestration for collect → analyze → decide → notify."""

from __future__ import annotations

import json
from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from agent.llm.bedrock import invoke_claude, parse_verdict_json
from agent.llm.prompts import build_messages
from agent.tools.docker_events import get_docker_events
from agent.tools.http_probe import probe_endpoints
from agent.tools.loki import fetch_loki_logs
from agent.tools.notify import send_push_notification
from agent.tools.prometheus import query_prometheus
from agent.tools.ssh_exec import execute_remote_command


class GraphState(TypedDict, total=False):
    collected: dict[str, Any]
    verdict: dict[str, Any]
    raw_llm: str
    llm_error: str | None
    ssh_context: dict[str, Any] | None
    notify_result: dict[str, Any] | None


def _collect_data(_: GraphState) -> dict[str, Any]:
    collected: dict[str, Any] = {
        "loki": fetch_loki_logs(),
        "prometheus": query_prometheus(),
        "docker": get_docker_events(),
        "http_probe": probe_endpoints(),
    }
    return {"collected": collected}


def _fallback_verdict(message: str) -> dict[str, Any]:
    return {
        "severity": "warning",
        "summary": "Analysis pipeline degraded; operator review required.",
        "root_cause": message,
        "recommended_action": "Verify Bedrock credentials, quotas, and network egress.",
    }


def _analyze(state: GraphState) -> dict[str, Any]:
    collected = state.get("collected") or {}
    system, user = build_messages(collected)
    llm = invoke_claude(system, user)
    if not llm.get("ok"):
        verdict = _fallback_verdict(str(llm.get("message", "unknown_error")))
        return {
            "raw_llm": "",
            "llm_error": str(llm.get("message")),
            "verdict": verdict,
        }

    parsed = parse_verdict_json(str(llm.get("text", "")))
    if not parsed.get("ok"):
        verdict = _fallback_verdict(str(parsed.get("message", "parse_error")))
        return {
            "raw_llm": str(llm.get("text", "")),
            "llm_error": str(parsed.get("message")),
            "verdict": verdict,
        }

    return {
        "raw_llm": str(llm.get("text", "")),
        "llm_error": None,
        "verdict": parsed["verdict"],
    }


def _decide_action(state: GraphState) -> dict[str, Any]:
    verdict = state.get("verdict") or {}
    if verdict.get("severity") == "critical":
        ssh = execute_remote_command()
        merged = dict(verdict)
        if ssh.get("ok"):
            merged["root_cause"] = merged.get("root_cause", "") + "\n\nSSH context:\n" + json.dumps(
                ssh, indent=2, default=str
            )
        else:
            merged["root_cause"] = merged.get("root_cause", "") + "\n\nSSH collection failed:\n" + json.dumps(
                ssh, indent=2, default=str
            )
        return {"ssh_context": ssh, "verdict": merged}
    return {"ssh_context": None}


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


def run_cycle() -> GraphState:
    """Execute one full orchestration cycle synchronously."""
    app = build_graph()
    result: GraphState = app.invoke({})
    return result

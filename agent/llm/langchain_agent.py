"""LangChain AgentExecutor wrapping Gemini via ChatVertexAI for multi-tool reasoning."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_vertexai import ChatVertexAI

from agent.tools.langchain_tools import ALL_TOOLS

_SYSTEM_PROMPT = """\
You are a senior SRE analyzing infrastructure telemetry for a self-hosted application.

You have access to three tools:
1. fetch_loki_logs_tool — queries Loki for recent application logs
2. fetch_prometheus_metrics_tool — queries Prometheus for CPU, memory, disk, and error rates
3. probe_http_endpoints_tool — probes HTTP endpoints for status and latency

RULES:
- Call ALL available tools to gather data before making your verdict.
- If a tool returns "not_configured", that integration is intentionally absent — do NOT flag it.
- Focus ONLY on the health of the monitored application based on the data you collect.
- Do NOT escalate severity because optional observability is missing.

After gathering all data, produce your final verdict as a JSON object with exactly these fields:
- severity: one of "ok", "warning", "high", "critical"
- summary: one sentence describing the current state
- root_cause: detailed analysis of what is wrong and why
- recommended_action: specific steps to resolve

Return ONLY the JSON verdict as your final answer, no markdown fences."""


def _extract_json(text: str) -> dict[str, Any] | None:
    """Extract JSON from agent output text."""
    text = text.strip()
    fence = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text, re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass
    # Try to find JSON object in text
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    return None


def run_langchain_agent(context: str = "") -> dict[str, Any]:
    """Run the LangChain agent with multi-tool reasoning and return a verdict dict.

    Args:
        context: Additional context to include in the prompt (e.g. docker events, log errors).

    Returns:
        A dict with ``ok: True`` and verdict fields, or ``ok: False`` with error info.
    """
    project = os.environ.get("GCP_PROJECT_ID", "").strip()
    region = os.environ.get("GCP_REGION", "us-central1").strip() or "us-central1"

    if not project:
        return {"ok": False, "error": "missing_env", "message": "GCP_PROJECT_ID is not set"}

    try:
        llm = ChatVertexAI(
            model_name="gemini-2.5-flash",
            project=project,
            location=region,
            temperature=0.2,
            max_output_tokens=2048,
        )

        llm_with_tools = llm.bind_tools(ALL_TOOLS)

        messages: list[Any] = [
            SystemMessage(content=_SYSTEM_PROMPT),
        ]

        if context:
            messages.append(HumanMessage(content=(
                "Here is additional context from Docker events and container logs:\n\n"
                f"{context}\n\n"
                "Now use your tools to gather more telemetry data, then produce your verdict."
            )))
        else:
            messages.append(HumanMessage(content=(
                "Analyze the current infrastructure health. "
                "Use your tools to gather telemetry data, then produce your verdict."
            )))

        # Agentic loop: call tools iteratively until the LLM produces a final answer
        max_iterations = 6
        for _ in range(max_iterations):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                break

            from langchain_core.messages import ToolMessage
            tool_map = {t.name: t for t in ALL_TOOLS}
            for tc in response.tool_calls:
                tool_fn = tool_map.get(tc["name"])
                if tool_fn:
                    result = tool_fn.invoke(tc["args"])
                    messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
                else:
                    messages.append(ToolMessage(
                        content=json.dumps({"error": f"Unknown tool: {tc['name']}"}),
                        tool_call_id=tc["id"],
                    ))

        # Extract verdict from final response
        final_text = str(response.content) if hasattr(response, "content") else ""
        if not final_text:
            return {"ok": False, "error": "empty_output", "message": "LangChain agent returned no text"}

        parsed = _extract_json(final_text)
        if not parsed:
            return {
                "ok": False,
                "error": "json_decode",
                "message": "Could not parse verdict JSON from agent output",
                "raw": final_text,
            }

        severity = str(parsed.get("severity", "")).lower()
        allowed = {"ok", "warning", "high", "critical"}
        if severity not in allowed:
            return {
                "ok": False,
                "error": "invalid_severity",
                "message": f"Got severity '{severity}'",
                "raw": parsed,
            }

        return {
            "ok": True,
            "severity": severity,
            "summary": str(parsed.get("summary", "")),
            "root_cause": str(parsed.get("root_cause", "")),
            "recommended_action": str(parsed.get("recommended_action", "")),
            "_raw_text": final_text,
        }

    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "langchain_agent_failed",
            "message": str(exc),
        }

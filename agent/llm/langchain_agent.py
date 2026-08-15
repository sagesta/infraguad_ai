"""LangChain multi-tool reasoning across supported direct model APIs."""

from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

from langchain_core.messages import HumanMessage, SystemMessage

from agent.llm.providers import active_model, llm_provider
from agent.llm.schema import VERDICT_OUTPUT_RULES, parse_verdict_text
from agent.tools.langchain_tools import ALL_TOOLS

_SYSTEM_PROMPT = f"""\
You are a senior SRE analyzing infrastructure telemetry for a self-hosted application.

You have access to three tools:
1. fetch_loki_logs_tool — queries Loki for recent application logs
2. fetch_prometheus_metrics_tool — queries Prometheus for CPU, memory, disk, and error rates
3. probe_http_endpoints_tool — probes HTTP endpoints for status and latency

RULES:
- Call ALL available tools to gather data before making your verdict.
- If a tool returns "not_configured", that integration is intentionally absent — do NOT flag it.
- Focus ONLY on the health of the monitored infrastructure based on Loki logs, Prometheus metrics, and HTTP probes.
- Docker container telemetry (events, error log lines) may be included in the provided context; assess it only when present. Never speculate about containers otherwise.

After gathering all data:
{VERDICT_OUTPUT_RULES}"""

def build_chat_model() -> Any | dict[str, Any]:
    """Construct the LangChain chat model for the configured provider.

    Returns the model instance, or an ``ok: False`` error dict when the
    provider is unconfigured/unknown (mirrors the single-call clients).
    Shared by the multi-tool verdict agent and the RAG runbook assistant, so
    both follow whichever LLM_PROVIDER is set — including a fully local Ollama.
    """
    provider = llm_provider()

    if provider == "gemini":
        api_key = (
            os.environ.get("GEMINI_API_KEY", "").strip()
            or os.environ.get("GOOGLE_API_KEY", "").strip()
        )
        if not api_key:
            return {"ok": False, "error": "missing_env", "message": "GEMINI_API_KEY is not set"}
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            return {
                "ok": False,
                "error": "missing_dependency",
                "message": "The 'langchain-google-genai' package is not installed",
            }
        return ChatGoogleGenerativeAI(
            model=active_model(),
            api_key=api_key,
            vertexai=False,
            temperature=0.2,
        )

    if provider == "ollama":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            return {
                "ok": False,
                "error": "missing_dependency",
                "message": "The 'langchain-openai' package is not installed",
            }
        base_url = os.environ.get("OLLAMA_BASE_URL", "").strip() or "http://ollama:11434/v1"
        # Ollama's OpenAI-compatible endpoint ignores the API key; a non-empty
        # placeholder is required because the client validates the field.
        return ChatOpenAI(model=active_model(), base_url=base_url, api_key="ollama")

    if provider == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
            return {"ok": False, "error": "missing_env", "message": "ANTHROPIC_API_KEY is not set"}
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError:
            return {
                "ok": False,
                "error": "missing_dependency",
                "message": "The 'langchain-anthropic' package is not installed",
            }
        # No temperature: removed on Claude Opus 5 (a non-default value 400s).
        return ChatAnthropic(model=active_model(), max_tokens=8192)

    if provider == "openai":
        if not os.environ.get("OPENAI_API_KEY", "").strip():
            return {"ok": False, "error": "missing_env", "message": "OPENAI_API_KEY is not set"}
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            return {
                "ok": False,
                "error": "missing_dependency",
                "message": "The 'langchain-openai' package is not installed",
            }
        # No temperature: reasoning-tier models reject non-default sampling params.
        return ChatOpenAI(model=active_model())

    return {
        "ok": False,
        "error": "unknown_provider",
        "message": f"LLM_PROVIDER '{provider}' is not one of gemini, anthropic, openai, ollama",
    }


def extract_raw_text(output: Any) -> str:
    """Extract raw text from a potential list of blocks."""
    if isinstance(output, list):
        for block in output:
            if isinstance(block, dict) and block.get('type') == 'text':
                return block.get('text', '')
        return str(output)
    return str(output)


def run_langchain_agent(context: str = "") -> dict[str, Any]:
    """Run the LangChain agent with multi-tool reasoning and return a verdict dict.

    Args:
        context: Additional context to include in the prompt (e.g. docker events, log errors).

    Returns:
        A dict with ``ok: True`` and verdict fields, or ``ok: False`` with error info.
    """
    llm_or_err = build_chat_model()
    if isinstance(llm_or_err, dict):
        return llm_or_err
    llm = llm_or_err

    try:
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
        raw = response.content if hasattr(response, "content") else ""
        if not raw:
            return {"ok": False, "error": "empty_output", "message": "LangChain agent returned no text"}

        if isinstance(raw, list):
            final_text = next((b['text'] for b in raw if isinstance(b, dict) and b.get('type') == 'text'), str(raw))
        else:
            final_text = str(raw)

        parsed = parse_verdict_text(final_text)
        if not parsed.get("ok"):
            logger.warning(
                "Could not parse verdict from agent output (%s). Raw (first 300 chars): %r",
                parsed.get("error"),
                final_text[:300],
            )
        return parsed

    except Exception as exc:  # noqa: BLE001
        logger.error("LLM Execution or Parsing Failed", exc_info=True)
        return {
            "ok": False,
            "error": "langchain_agent_failed",
            "message": str(exc),
        }

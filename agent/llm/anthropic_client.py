"""Anthropic Claude client for JSON verdict generation (LLM_PROVIDER=anthropic)."""

from __future__ import annotations

import logging
import os
from typing import Any

from agent.llm.schema import VERDICT_SYSTEM_INSTRUCTION, parse_verdict_text

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-5"


def _model() -> str:
    return os.environ.get("ANTHROPIC_MODEL", "").strip() or DEFAULT_MODEL


def get_verdict(context: str) -> dict[str, Any]:
    """Call the Anthropic Messages API and return a parsed verdict dict.

    Mirrors the shared provider contract: never raises; returns ``ok: False``
    with ``error``/``message`` on any failure so the orchestrator can degrade
    to its fallback verdict.
    """
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        return {"ok": False, "error": "missing_env", "message": "ANTHROPIC_API_KEY is not set"}

    try:
        import anthropic
    except ImportError:
        return {
            "ok": False,
            "error": "missing_dependency",
            "message": "The 'anthropic' package is not installed (pip install anthropic)",
        }

    try:
        client = anthropic.Anthropic()
        # No temperature/top_p for adaptive-thinking Claude 5 models, and
        # no thinking config (adaptive thinking is the default). max_tokens caps
        # thinking + answer together, so it needs headroom beyond the JSON verdict.
        response = client.messages.create(
            model=_model(),
            max_tokens=16000,
            system=VERDICT_SYSTEM_INSTRUCTION,
            messages=[{"role": "user", "content": context}],
        )
    except anthropic.RateLimitError as exc:
        return {"ok": False, "error": "rate_limited", "message": str(exc)}
    except anthropic.APIStatusError as exc:
        return {"ok": False, "error": "anthropic_api_error", "message": f"{exc.status_code}: {exc.message}"}
    except anthropic.APIConnectionError as exc:
        return {"ok": False, "error": "network_error", "message": str(exc)}
    except Exception as exc:  # noqa: BLE001
        logger.error("Anthropic verdict call failed", exc_info=True)
        return {"ok": False, "error": "anthropic_failed", "message": str(exc)}

    # Safety classifiers can decline with a 200 + refusal stop reason; the
    # content is empty or partial, so treat it as a failed cycle, not a verdict.
    if response.stop_reason == "refusal":
        return {
            "ok": False,
            "error": "refusal",
            "message": "Model declined the request (safety classifiers)",
        }

    text = next((b.text for b in response.content if b.type == "text"), "")
    return parse_verdict_text(text)

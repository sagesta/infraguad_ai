"""OpenAI client for JSON verdict generation (LLM_PROVIDER=openai)."""

from __future__ import annotations

import logging
import os
from typing import Any

from agent.llm.schema import VERDICT_SYSTEM_INSTRUCTION, parse_verdict_text

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-5.1"


def _model() -> str:
    return os.environ.get("OPENAI_MODEL", "").strip() or DEFAULT_MODEL


def get_verdict(context: str) -> dict[str, Any]:
    """Call the OpenAI Chat Completions API and return a parsed verdict dict.

    Mirrors the shared provider contract: never raises; returns ``ok: False``
    with ``error``/``message`` on any failure so the orchestrator can degrade
    to its fallback verdict.
    """
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        return {"ok": False, "error": "missing_env", "message": "OPENAI_API_KEY is not set"}

    try:
        import openai
    except ImportError:
        return {
            "ok": False,
            "error": "missing_dependency",
            "message": "The 'openai' package is not installed (pip install openai)",
        }

    try:
        client = openai.OpenAI()
        # No temperature override: reasoning-tier models reject non-default
        # sampling params. json_object mode enforces a parseable body.
        response = client.chat.completions.create(
            model=_model(),
            messages=[
                {"role": "system", "content": VERDICT_SYSTEM_INSTRUCTION},
                {"role": "user", "content": context},
            ],
            response_format={"type": "json_object"},
        )
    except openai.RateLimitError as exc:
        return {"ok": False, "error": "rate_limited", "message": str(exc)}
    except openai.APIStatusError as exc:
        return {"ok": False, "error": "openai_api_error", "message": f"{exc.status_code}: {exc.message}"}
    except openai.APIConnectionError as exc:
        return {"ok": False, "error": "network_error", "message": str(exc)}
    except Exception as exc:  # noqa: BLE001
        logger.error("OpenAI verdict call failed", exc_info=True)
        return {"ok": False, "error": "openai_failed", "message": str(exc)}

    text = (response.choices[0].message.content or "") if response.choices else ""
    return parse_verdict_text(text)

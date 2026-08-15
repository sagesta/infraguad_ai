"""Ollama client for JSON verdict generation (LLM_PROVIDER=ollama).

Ollama serves an OpenAI-compatible endpoint, so this reuses the ``openai``
SDK rather than adding a dedicated Ollama dependency — pointed at a local
base URL instead of api.openai.com, with no API key required.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from agent.llm.schema import VERDICT_SYSTEM_INSTRUCTION, parse_verdict_text

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_BASE_URL = "http://ollama:11434/v1"


def _model() -> str:
    return os.environ.get("OLLAMA_MODEL", "").strip() or DEFAULT_MODEL


def _base_url() -> str:
    return os.environ.get("OLLAMA_BASE_URL", "").strip() or DEFAULT_BASE_URL


def get_verdict(context: str) -> dict[str, Any]:
    """Call a local Ollama server and return a parsed verdict dict.

    Mirrors the other providers' contract: never raises; returns ``ok: False``
    with ``error``/``message`` on any failure so the orchestrator can degrade
    to its fallback verdict. No ``response_format`` is forced — Ollama's
    JSON-mode support varies by model/version, so this relies on the shared
    parser's tolerance for fenced or prose-wrapped JSON instead.
    """
    try:
        import openai
    except ImportError:
        return {
            "ok": False,
            "error": "missing_dependency",
            "message": "The 'openai' package is not installed (pip install openai)",
        }

    try:
        # api_key is a required non-empty field for the SDK but is ignored by
        # Ollama's compatibility layer — there is no account or key to manage.
        client = openai.OpenAI(base_url=_base_url(), api_key="ollama")
        response = client.chat.completions.create(
            model=_model(),
            messages=[
                {"role": "system", "content": VERDICT_SYSTEM_INSTRUCTION},
                {"role": "user", "content": context},
            ],
        )
    except openai.APIConnectionError as exc:
        return {
            "ok": False,
            "error": "network_error",
            "message": f"Could not reach Ollama at {_base_url()}: {exc}",
        }
    except openai.APIStatusError as exc:
        return {"ok": False, "error": "ollama_api_error", "message": f"{exc.status_code}: {exc.message}"}
    except Exception as exc:  # noqa: BLE001
        logger.error("Ollama verdict call failed", exc_info=True)
        return {"ok": False, "error": "ollama_failed", "message": str(exc)}

    text = (response.choices[0].message.content or "") if response.choices else ""
    return parse_verdict_text(text)

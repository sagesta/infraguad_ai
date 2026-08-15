"""Direct Gemini Developer API client (``LLM_PROVIDER=gemini``)."""

from __future__ import annotations

import logging
import os
from typing import Any

from google import genai
from google.genai.types import GenerateContentConfig

from agent.llm.schema import VERDICT_SYSTEM_INSTRUCTION, parse_verdict_text

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gemini-3.6-flash"


def _api_key() -> str:
    """Return the direct Gemini API key, accepting Google's common alias."""
    return (
        os.environ.get("GEMINI_API_KEY", "").strip()
        or os.environ.get("GOOGLE_API_KEY", "").strip()
    )


def _model() -> str:
    return os.environ.get("GEMINI_MODEL", "").strip() or DEFAULT_MODEL


def get_verdict(context: str) -> dict[str, Any]:
    """Call Gemini directly and return the normalized verdict contract."""
    api_key = _api_key()
    if not api_key:
        return {
            "ok": False,
            "error": "missing_env",
            "message": "GEMINI_API_KEY is not set",
        }

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=_model(),
            contents=context,
            config=GenerateContentConfig(
                system_instruction=VERDICT_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        text = (response.text or "").strip()
    except Exception as exc:  # noqa: BLE001
        logger.error("Gemini verdict call failed", exc_info=True)
        return {
            "ok": False,
            "error": "gemini_generate_failed",
            "message": str(exc),
        }

    return parse_verdict_text(text)

"""Google Vertex AI (Gemini) client for JSON verdict generation."""

from __future__ import annotations

import json
import os
import re
from typing import Any

import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel

MODEL_NAME = "gemini-2.0-flash"

_model: GenerativeModel | None = None


def _extract_json_text(text: str) -> str:
    text = text.strip()
    fence = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text, re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    return text


def _validate_verdict(data: dict[str, Any]) -> dict[str, Any]:
    severity = str(data.get("severity", "")).lower()
    allowed = {"ok", "warning", "high", "critical"}
    if severity not in allowed:
        return {
            "ok": False,
            "error": "invalid_severity",
            "message": severity,
            "raw": data,
        }
    return {
        "ok": True,
        "verdict": {
            "severity": severity,
            "summary": str(data.get("summary", "")),
            "root_cause": str(data.get("root_cause", "")),
            "recommended_action": str(data.get("recommended_action", "")),
        },
    }


def _ensure_model() -> dict[str, Any] | GenerativeModel:
    """Initialize Vertex once and return the model, or an error dict."""
    global _model
    if _model is not None:
        return _model

    project = os.environ.get("GCP_PROJECT_ID", "").strip()
    if not project:
        return {
            "ok": False,
            "error": "missing_env",
            "message": "GCP_PROJECT_ID is not set",
        }

    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    if not creds:
        return {
            "ok": False,
            "error": "missing_env",
            "message": "GOOGLE_APPLICATION_CREDENTIALS is not set",
        }

    region = os.environ.get("GCP_REGION", "us-central1").strip() or "us-central1"

    try:
        vertexai.init(project=project, location=region)
        _model = GenerativeModel(MODEL_NAME)
        return _model
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "vertex_init_failed",
            "message": str(exc),
        }


def get_verdict(context: str) -> dict[str, Any]:
    """
    Call Vertex AI Gemini with the assembled prompt and return a parsed verdict dict.

    On success, returns keys: severity, summary, root_cause, recommended_action.

    On failure, returns a structured error dict with ``ok: False`` and a ``message`` field
    (does not raise).
    """
    model_or_err = _ensure_model()
    if isinstance(model_or_err, dict):
        return model_or_err

    model = model_or_err

    try:
        response = model.generate_content(
            context,
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )
        text = (response.text or "").strip()
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "vertex_generate_failed",
            "message": str(exc),
        }

    if not text:
        return {"ok": False, "error": "empty_output", "message": "Model returned no text"}

    try:
        cleaned = _extract_json_text(text)
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "error": "json_decode",
            "message": str(exc),
            "raw": text,
        }

    if not isinstance(data, dict):
        return {
            "ok": False,
            "error": "invalid_shape",
            "message": "Model JSON was not an object",
            "raw": data,
        }

    validated = _validate_verdict(data)
    if not validated.get("ok"):
        return {
            "ok": False,
            "error": str(validated.get("error")),
            "message": str(validated.get("message")),
            "raw": validated.get("raw"),
        }

    verdict = validated["verdict"]
    out: dict[str, Any] = dict(verdict)
    out["ok"] = True
    out["_raw_text"] = text
    return out

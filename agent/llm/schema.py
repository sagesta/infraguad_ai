"""Shared LLM verdict contract: system instruction, JSON extraction, validation.

Every provider client (Gemini, Anthropic Claude, OpenAI) and both
reasoning modes import from this module, so the verdict schema and signature
rules cannot drift between backends.
"""

from __future__ import annotations

import json
import re
from typing import Any

ALLOWED_SEVERITIES = {"ok", "warning", "high", "critical"}

# The output half of the contract — shared verbatim by the single-call system
# instruction below and by the LangChain agent's system prompt.
VERDICT_OUTPUT_RULES = (
    "Produce your verdict as a JSON object with exactly these fields:\n"
    '- severity: one of "ok", "warning", "high", "critical"\n'
    "- summary: one sentence describing the current state\n"
    "- root_cause: detailed analysis of what is wrong and why\n"
    "- recommended_action: specific steps to resolve\n"
    '- signature: a short, STABLE identifier of the condition formatted "<source>:<condition>:<resource>" '
    '(e.g. "prometheus:disk-low:/", "loki:error-spike:devplanner-api"), reused verbatim whenever the same '
    'underlying condition recurs; use "none:healthy:all" when severity is "ok". If the context lists '
    'operator-acknowledged known conditions and the current state matches one unchanged, return severity "ok" '
    "and reuse its signature.\n"
    "You must return ONLY raw, valid JSON. Under no circumstances should you utilize markdown code blocks, "
    "backticks, or append any conversational dialogue."
)

VERDICT_SYSTEM_INSTRUCTION = (
    "You are an SRE analyzing live infrastructure telemetry. "
    "Only assess components explicitly present in the context data. "
    "Do not flag absent, unconfigured, or optional tools (such as Loki, Prometheus, Docker monitoring, "
    "or any monitoring stack) as issues — if they are not in the context, they do not exist in this deployment. "
    "Focus ONLY on the health of the monitored infrastructure based on the telemetry sections provided "
    "(Loki logs, Prometheus metrics, HTTP probes, and Docker events/log lines when present). "
    "Docker container data is in scope only when a DOCKER section appears in the context; never speculate "
    "about containers otherwise. "
    "If all present components are healthy, return severity 'ok'. "
    "Base your verdict ONLY on the data provided, nothing else.\n\n" + VERDICT_OUTPUT_RULES
)


def extract_json_text(text: str) -> str:
    """Strip markdown code fences and other wrapping from LLM JSON output."""
    text = text.strip()
    fence = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text, re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    return text.strip()


def parse_verdict_text(text: str) -> dict[str, Any]:
    """Parse raw model output into the normalized verdict result dict.

    Returns ``{"ok": True, severity, summary, root_cause, recommended_action,
    signature, "_raw_text"}`` on success, or ``{"ok": False, "error", "message"}``
    (never raises). Tolerates code fences and surrounding prose.
    """
    raw = (text or "").strip()
    if not raw:
        return {"ok": False, "error": "empty_output", "message": "Model returned no text"}

    cleaned = extract_json_text(raw)
    data: Any = None
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to the outermost JSON object embedded in prose.
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                data = None
    if data is None:
        return {
            "ok": False,
            "error": "json_decode",
            "message": "Could not parse verdict JSON from model output",
            "raw": raw,
        }
    if not isinstance(data, dict):
        return {
            "ok": False,
            "error": "invalid_shape",
            "message": "Model JSON was not an object",
            "raw": data,
        }

    severity = str(data.get("severity", "")).lower()
    if severity not in ALLOWED_SEVERITIES:
        return {
            "ok": False,
            "error": "invalid_severity",
            "message": f"Got severity '{severity}'",
            "raw": data,
        }

    return {
        "ok": True,
        "severity": severity,
        "summary": str(data.get("summary", "")),
        "root_cause": str(data.get("root_cause", "")),
        "recommended_action": str(data.get("recommended_action", "")),
        "signature": str(data.get("signature", "")),
        "_raw_text": raw,
    }

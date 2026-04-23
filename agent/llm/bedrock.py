"""AWS Bedrock client for Claude Haiku."""

from __future__ import annotations

import json
import os
import re
from typing import Any

import boto3


MODEL_ID = "anthropic.claude-haiku-20240307-v1:0"


def _extract_json_text(text: str) -> str:
    text = text.strip()
    fence = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text, re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    return text


def invoke_claude(system_prompt: str, user_message: str) -> dict[str, Any]:
    """
    Invoke Claude Haiku on AWS Bedrock and return assistant text or structured error.
    """
    region = os.environ.get("AWS_REGION", "").strip()
    key_id = os.environ.get("AWS_ACCESS_KEY_ID", "").strip()
    secret = os.environ.get("AWS_SECRET_ACCESS_KEY", "").strip()

    if not region or not key_id or not secret:
        return {
            "ok": False,
            "error": "missing_env",
            "message": "AWS_REGION, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY must be set",
        }

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "temperature": 0.2,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_message}],
                }
            ],
        }
    )

    try:
        client = boto3.client(
            "bedrock-runtime",
            region_name=region,
            aws_access_key_id=key_id,
            aws_secret_access_key=secret,
        )
        resp = client.invoke_model(
            modelId=MODEL_ID,
            body=body,
            contentType="application/json",
            accept="application/json",
        )
        raw = resp["body"].read().decode("utf-8")
        payload = json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "bedrock_invoke_failed",
            "message": str(exc),
        }

    try:
        parts = payload.get("content", [])
        texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
        text = "\n".join(t for t in texts if t)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "parse_response",
            "message": str(exc),
            "raw": payload,
        }

    if not text:
        return {"ok": False, "error": "empty_output", "message": "Model returned no text"}

    return {"ok": True, "text": text}


def parse_verdict_json(llm_text: str) -> dict[str, Any]:
    """Parse model JSON verdict; returns ok dict or error dict."""
    try:
        cleaned = _extract_json_text(llm_text)
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "error": "json_decode",
            "message": str(exc),
            "raw": llm_text,
        }

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

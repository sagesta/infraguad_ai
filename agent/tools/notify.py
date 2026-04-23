"""Push notifications via ntfy.sh."""

from __future__ import annotations

import os
from typing import Any, Literal

import httpx

Severity = Literal["ok", "warning", "high", "critical"]

PRIORITY_MAP: dict[str, str] = {
    "ok": "min",
    "warning": "default",
    "high": "high",
    "critical": "urgent",
}


def send_push_notification(
    title: str,
    message: str,
    severity: Severity | str = "warning",
) -> dict[str, Any]:
    """
    POST a notification to https://ntfy.sh/{NTFY_TOPIC} with title, body, and priority.
    """
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    if not topic:
        return {"ok": False, "error": "missing_env", "message": "NTFY_TOPIC is not set"}

    url = f"https://ntfy.sh/{topic}"
    priority = PRIORITY_MAP.get(str(severity), "default")
    headers = {
        "Title": title,
        "Priority": priority,
    }

    try:
        with httpx.Client(timeout=20.0) as client:
            resp = client.post(url, content=message, headers=headers)
            resp.raise_for_status()
    except httpx.HTTPError as exc:
        return {
            "ok": False,
            "error": "http_error",
            "message": str(exc),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "error": "unexpected",
            "message": str(exc),
        }

    return {"ok": True, "status_code": resp.status_code}

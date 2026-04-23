"""Docker events tool (local socket or TCP DOCKER_HOST)."""

from __future__ import annotations

import json
import os
import time
from typing import Any

import httpx


def get_docker_events() -> dict[str, Any]:
    """
    Fetch Docker events from the last 60 seconds.

    Flags container restarts and unhealthy transitions when present in event payloads.
    """
    docker_host = os.environ.get("DOCKER_HOST", "").strip()
    unix_socket = "/var/run/docker.sock"

    transport: httpx.BaseTransport | None = None
    base_url: str

    if docker_host.startswith("unix://"):
        sock_path = docker_host.removeprefix("unix://")
        transport = httpx.HTTPTransport(uds=sock_path)
        base_url = "http://docker"
    elif docker_host.startswith("tcp://"):
        base_url = docker_host.replace("tcp://", "http://")
    else:
        if os.path.exists(unix_socket):
            transport = httpx.HTTPTransport(uds=unix_socket)
            base_url = "http://docker"
        else:
            return {
                "ok": False,
                "error": "no_docker",
                "message": "DOCKER_HOST not set and /var/run/docker.sock not available",
            }

    since = int(time.time()) - 60
    url = f"{base_url}/v1.45/events"
    params = {"since": str(since), "until": str(int(time.time()))}

    events: list[dict[str, Any]] = []
    flags: dict[str, list[str]] = {"restarts": [], "unhealthy": [], "other": []}

    try:
        with httpx.Client(timeout=10.0, transport=transport) as client:
            with client.stream("GET", url, params=params) as resp:
                resp.raise_for_status()
                buffer = b""
                for chunk in resp.iter_bytes():
                    buffer += chunk
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        if not line.strip():
                            continue
                        try:
                            evt = json.loads(line.decode("utf-8"))
                        except json.JSONDecodeError:
                            continue
                        events.append(evt)
                        etype = evt.get("Type") or evt.get("type")
                        action = evt.get("Action") or evt.get("action")
                        actor = evt.get("Actor", {})
                        name = (
                            actor.get("Attributes", {}).get("name")
                            or actor.get("ID")
                            or "unknown"
                        )
                        if etype == "container" and action in ("restart", "die", "oom"):
                            flags["restarts"].append(f"{name}:{action}")
                        if "health_status: unhealthy" in json.dumps(evt):
                            flags["unhealthy"].append(name)
                        if len(events) >= 200:
                            break
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

    return {
        "ok": True,
        "events": events[-100:],
        "flags": flags,
        "count": len(events),
    }

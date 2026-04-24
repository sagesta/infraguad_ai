"""Docker events tool (local socket or TCP DOCKER_HOST)."""

from __future__ import annotations

import json
import os
import time
from typing import Any

import httpx

# Compose-style names for this stack; die/kill/destroy on these are usually deploy noise.
_SELF_CONTAINER_PREFIXES = ("infraguad_ai-agent", "infraguad_ai-api")

_EVENTS_WINDOW_SEC = 300


def _monitored_names() -> list[str]:
    raw = os.environ.get("MONITORED_CONTAINERS", "").strip()
    if not raw:
        return []
    return [n.strip().lstrip("/") for n in raw.split(",") if n.strip()]


def _is_self_container(name: str) -> bool:
    n = name.lstrip("/")
    return n.startswith(_SELF_CONTAINER_PREFIXES)


def _name_matches_monitored(name: str, monitored: list[str]) -> bool:
    n = name.lstrip("/")
    for m in monitored:
        m = m.lstrip("/")
        if n == m or n.startswith(f"{m}-") or n.startswith(f"{m}_"):
            return True
    return False


def _should_omit_event(etype: str, action: str, name: str, monitored: list[str]) -> bool:
    """Drop self-referential deploy noise and off-target die/kill/destroy when MONITORED_* is set."""
    if etype != "container":
        return False
    if action in ("die", "kill", "destroy"):
        if _is_self_container(name):
            return True
        if monitored and not _name_matches_monitored(name, monitored):
            return True
    if action == "restart" and _is_self_container(name):
        return True
    return False


def get_docker_events() -> dict[str, Any]:
    """
    Fetch Docker events from roughly the last five minutes.

    Flags container restarts and unhealthy transitions when present in event payloads.
    die/kill/destroy for InfraGuard's own agent/api containers are omitted (deploy noise).
    die/kill/destroy for containers not in MONITORED_CONTAINERS are omitted when that env is set.
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

    now = int(time.time())
    since = now - _EVENTS_WINDOW_SEC
    url = f"{base_url}/v1.45/events"
    params = {"since": str(since), "until": str(now)}

    events: list[dict[str, Any]] = []
    flags: dict[str, list[str]] = {"restarts": [], "unhealthy": [], "other": []}
    monitored = _monitored_names()

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

                        etype = str(evt.get("Type") or evt.get("type") or "").lower()
                        action = str(evt.get("Action") or evt.get("action") or "").lower()
                        actor = evt.get("Actor", {})
                        name = (
                            actor.get("Attributes", {}).get("name")
                            or actor.get("ID")
                            or "unknown"
                        )

                        if _should_omit_event(etype, action, name, monitored):
                            continue

                        events.append(evt)

                        if etype == "container" and action in ("restart", "die", "oom", "kill", "destroy"):
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

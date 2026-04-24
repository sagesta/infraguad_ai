"""Local Docker diagnostics via the Engine API (unix socket or DOCKER_HOST)."""

from __future__ import annotations

import os
from typing import Any

import docker
from docker.errors import APIError, DockerException, NotFound

_LOG_TAIL = 50


def _monitored_names() -> list[str]:
    raw = os.environ.get("MONITORED_CONTAINERS", "").strip()
    if not raw:
        return []
    return [n.strip() for n in raw.split(",") if n.strip()]


def collect_container_diagnostics() -> dict[str, Any]:
    """
    Stats, recent logs, and health for MONITORED_CONTAINERS (comma-separated names).

    Uses ``docker.from_env()`` (``DOCKER_HOST`` or default ``unix:///var/run/docker.sock``).
    """
    names = _monitored_names()
    if not names:
        return {
            "ok": False,
            "error": "missing_env",
            "message": "MONITORED_CONTAINERS must be set (comma-separated container names)",
        }

    try:
        client = docker.from_env()
    except DockerException as exc:
        return {"ok": False, "error": "docker_client", "message": str(exc)}

    out: dict[str, Any] = {"ok": True, "monitored": [], "containers_list": None, "list_error": None}

    try:
        for name in names:
            entry: dict[str, Any] = {"name": name}
            try:
                container = client.containers.get(name)
            except NotFound:
                entry["error"] = "not_found"
                out["monitored"].append(entry)
                continue
            except APIError as exc:
                entry["error"] = "api_error"
                entry["message"] = str(exc)
                out["monitored"].append(entry)
                continue

            attrs = container.attrs
            state = attrs.get("State") or {}
            health = state.get("Health")
            entry["status"] = state.get("Status")
            if health is not None:
                log = health.get("Log") or []
                entry["health"] = {
                    "status": health.get("Status"),
                    "failing_streak": health.get("FailingStreak"),
                    "log": log[-5:] if isinstance(log, list) else log,
                }

            try:
                entry["stats"] = container.stats(stream=False)
            except (APIError, DockerException) as exc:
                entry["stats_error"] = str(exc)

            try:
                raw_logs = container.logs(tail=_LOG_TAIL, timestamps=True)
                entry["logs_tail"] = (
                    raw_logs.decode("utf-8", errors="replace")
                    if isinstance(raw_logs, (bytes, bytearray))
                    else str(raw_logs)
                )
            except (APIError, DockerException) as exc:
                entry["logs_error"] = str(exc)

            entry["image"] = attrs.get("Config", {}).get("Image") or attrs.get("Image", "")
            out["monitored"].append(entry)

        try:
            all_cs = client.containers.list(all=True)
            out["containers_list"] = [
                {"id": c.short_id, "name": c.name or "", "status": c.status} for c in all_cs
            ]
        except (APIError, DockerException) as exc:
            out["list_error"] = str(exc)

    finally:
        client.close()

    return out

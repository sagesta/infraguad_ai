"""Filtered error lines from a Docker container's logs (Engine API, no app HTTP)."""

from __future__ import annotations

import asyncio
import logging
import docker
from docker.errors import APIError, DockerException, NotFound

logger = logging.getLogger(__name__)

_ERROR_MARKERS: tuple[str, ...] = (
    "error",
    "exception",
    "fatal",
    "failed",
    "5xx",
    "500",
    "traceback",
    "unhandledrejection",
)


def _line_matches_error(line: str) -> bool:
    lower = line.lower()
    return any(m in lower for m in _ERROR_MARKERS)


def _split_timestamp(line: str) -> tuple[str, str]:
    """Split Docker ``timestamps=True`` prefix (``...Z message``) from the log message."""
    line = line.strip()
    if not line:
        return "", ""
    sp = line.find(" ")
    if sp > 10 and line[0].isdigit() and "T" in line[:sp]:
        return line[:sp], line[sp + 1 :].strip()
    return "", line


def _fetch_container_errors_sync(container_name: str, tail: int) -> list[dict[str, str]]:
    name = container_name.strip()
    if not name:
        logger.warning("fetch_container_errors: empty container name, skipping")
        return []

    client = None
    try:
        client = docker.from_env()
    except DockerException as exc:
        logger.warning("fetch_container_errors: Docker client unavailable: %s", exc)
        return []

    try:
        try:
            container = client.containers.get(name)
        except NotFound:
            logger.warning("fetch_container_errors: container %r not found", name)
            return []
        except APIError as exc:
            logger.warning("fetch_container_errors: API error getting container %r: %s", name, exc)
            return []

        try:
            raw = container.logs(tail=tail, timestamps=True)
        except (APIError, DockerException) as exc:
            logger.warning("fetch_container_errors: failed to read logs for %r: %s", name, exc)
            return []

    finally:
        if client is not None:
            try:
                client.close()
            except Exception:  # noqa: BLE001
                pass

    text = raw.decode("utf-8", errors="replace") if isinstance(raw, (bytes, bytearray)) else str(raw)
    out: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        if not _line_matches_error(raw_line):
            continue
        ts, content = _split_timestamp(raw_line)
        out.append({"timestamp": ts, "line": content if ts else raw_line.strip()})
    return out


async def fetch_container_errors(container_name: str, tail: int = 100) -> list[dict[str, str]]:
    """
    Return recent log lines from *container_name* that look like errors (keyword filter).

    Runs blocking Docker SDK work in a thread pool. On failure, returns ``[]`` and logs a warning.
    """
    try:
        return await asyncio.to_thread(_fetch_container_errors_sync, container_name, tail)
    except Exception as exc:  # noqa: BLE001
        logger.warning("fetch_container_errors: unexpected error: %s", exc)
        return []

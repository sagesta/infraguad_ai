"""Provider-neutral prompt assembly for SRE verdicts."""

from __future__ import annotations

import json
from typing import Any


def _include_http_probe_block(collected: dict[str, Any]) -> bool:
    if "http_probe" not in collected:
        return False
    probe = collected["http_probe"]
    if not isinstance(probe, dict):
        return True
    # Skip empty dicts (unconfigured) and missing_env sentinels
    if not probe:
        return False
    return not (probe.get("ok") is False and probe.get("error") == "missing_env")


def _include_docker_logs_block(collected: dict[str, Any]) -> bool:
    logs = collected.get("docker_logs")
    return isinstance(logs, list) and len(logs) > 0


def _include_docker_events_block(collected: dict[str, Any]) -> bool:
    """Docker events are included only when monitoring is enabled and configured.

    A ``note`` key marks the disabled/unconfigured sentinel from the collector.
    """
    docker = collected.get("docker")
    if not isinstance(docker, dict):
        return False
    if docker.get("note"):
        return False
    return bool(docker.get("ok"))


def _known_conditions_block(known_conditions: list[dict[str, Any]] | None) -> str:
    """Render operator-acknowledged conditions so the agent can recognise them.

    This is the 'memory' fed back into the loop: conditions a human has already
    triaged and accepted, so the model stops re-flagging them unless they change.
    """
    if not known_conditions:
        return ""
    lines: list[str] = []
    for kc in known_conditions:
        sig = str(kc.get("signature") or "").strip()
        if not sig:
            continue
        note = str(kc.get("note") or "").strip()
        lines.append(f"- {sig}" + (f" — operator note: {note}" if note else ""))
    if not lines:
        return ""
    return (
        "OPERATOR-ACKNOWLEDGED KNOWN CONDITIONS (already triaged and accepted as non-issues; "
        "do NOT re-flag or escalate these unless the underlying condition has materially changed, "
        "e.g. a worse metric band or a new error class). If a current observation matches one of "
        "these and has not materially changed, return severity \"ok\" and reuse its signature:\n"
        + "\n".join(lines)
        + "\n\n"
    )


def assemble_prompt_from_collected(
    collected: dict[str, Any],
    known_conditions: list[dict[str, Any]] | None = None,
) -> str:
    """Serialize tool outputs into telemetry blocks for the configured model.

    Loki and Prometheus sections appear only when present in ``collected``.
    HTTP probe is skipped when absent or when the payload is only a PROBE_URLS
    ``missing_env`` sentinel. Docker events appear only when local Docker
    monitoring is enabled; Docker log errors appear only when the list is non-empty.
    ``known_conditions`` are operator acknowledgements injected as memory.
    """
    blocks: list[str] = []

    if "loki" in collected:
        blocks.append(
            "=== LOGS (last 50 lines) ===\n" + json.dumps(collected["loki"], indent=2, default=str)
        )
    if "prometheus" in collected:
        blocks.append(
            "=== METRICS (CPU/RAM/Disk) ===\n"
            + json.dumps(collected["prometheus"], indent=2, default=str)
        )

    if _include_http_probe_block(collected):
        blocks.append(
            "=== HTTP PROBE RESULTS ===\n" + json.dumps(collected["http_probe"], indent=2, default=str)
        )

    if _include_docker_events_block(collected):
        blocks.append(
            "=== DOCKER EVENTS (last 5 min) ===\n"
            + json.dumps(collected["docker"], indent=2, default=str)
        )

    if _include_docker_logs_block(collected):
        blocks.append(
            "=== DOCKER CONTAINER ERROR LINES ===\n"
            + json.dumps(collected["docker_logs"], indent=2, default=str)
        )

    telemetry = "\n\n".join(blocks)
    known_block = _known_conditions_block(known_conditions)

    return f"""
You are a senior SRE analyzing infrastructure telemetry for a self-hosted application.

CRITICAL RULES:
1. Only the telemetry sections below are in scope. If LOGS, METRICS, HTTP PROBE, or DOCKER sections are absent, that means those integrations are NOT deployed — this is normal and expected, NOT an incident. Do NOT mention absent sections.
2. Do NOT escalate severity because an optional observability component (Loki, Prometheus, Docker monitoring, log aggregation, metrics collection) is missing. Their absence is a deliberate configuration choice.
3. DNS resolution errors in HTTP probes to internal Docker hostnames (e.g. "devplanner-api") indicate a Docker networking issue between containers, not a widespread DNS failure.
4. Focus ONLY on the health of the monitored application itself based on the data present.

Return ONLY valid JSON with these fields:
- severity: one of "ok", "warning", "high", "critical"
- summary: one sentence describing current state
- root_cause: detailed analysis of what is wrong and why
- recommended_action: specific steps to resolve
- signature: a short, STABLE identifier of the condition, formatted "<source>:<condition>:<resource>" (e.g. "prometheus:disk-low:/", "loki:error-spike:devplanner-api", "probe:endpoint-down:api.example.com"). Reuse the EXACT same signature whenever the SAME underlying condition recurs across checks, so repeat occurrences are recognisable. Use "none:healthy:all" when severity is "ok".

{known_block}TELEMETRY DATA:

{telemetry}
"""

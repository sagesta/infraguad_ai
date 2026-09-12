"""Threat detection and CrowdSec integration stub."""

from __future__ import annotations

import ipaddress
import logging
import os
import re
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Patterns for threat detection
_BRUTE_FORCE_THRESHOLD = 10
_PORT_SCAN_THRESHOLD = 20
ALLOWED_CROWDSEC_THREAT_TYPES = frozenset(
    {"http_brute_force", "ssh_brute_force", "port_scan"}
)


def _extract_ips(text: str) -> list[str]:
    """Extract IPv4 addresses from text."""
    valid: list[str] = []
    for candidate in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text):
        try:
            valid.append(str(ipaddress.IPv4Address(candidate)))
        except ipaddress.AddressValueError:
            continue
    return valid


def _validated_crowdsec_ip(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("source_ip must be a valid IP address string")
    try:
        address = ipaddress.ip_address(value.strip())
    except ValueError as exc:
        raise ValueError("source_ip must be a valid IP address string") from exc

    # Apply the same policy to IPv4-mapped IPv6 addresses so ::ffff:127.0.0.1
    # cannot bypass the loopback check. Private addresses remain valid because
    # InfraGuard may monitor private or VPN infrastructure.
    policy_address = getattr(address, "ipv4_mapped", None) or address
    if policy_address.is_loopback:
        raise ValueError("source_ip must not be a loopback address")
    if policy_address.is_link_local:
        raise ValueError("source_ip must not be a link-local address")
    if policy_address.is_multicast:
        raise ValueError("source_ip must not be a multicast address")
    if policy_address.is_unspecified:
        raise ValueError("source_ip must not be an unspecified address")
    return str(address)


def analyze_threats(loki_logs: list[dict[str, Any]]) -> dict[str, Any]:
    """Detect threat patterns in log lines.

    Looks for:
    - Repeated 401/403 responses (brute force)
    - SSH auth failures (auth.log patterns)
    - Port scan signatures

    Args:
        loki_logs: List of log line dicts with 'line' and optional 'labels' keys.

    Returns:
        Dict with threat analysis results.
    """
    threats: list[dict[str, Any]] = []
    ip_401_count: dict[str, int] = {}
    ip_ssh_fail: dict[str, int] = {}
    ip_connection: dict[str, int] = {}

    for entry in loki_logs:
        line = str(entry.get("line", ""))
        line_lower = line.lower()

        # Detect repeated 401/403 — HTTP brute force
        if " 401 " in line or " 403 " in line or "unauthorized" in line_lower:
            for ip in _extract_ips(line):
                ip_401_count[ip] = ip_401_count.get(ip, 0) + 1

        # Detect SSH brute force (auth.log patterns)
        if "failed password" in line_lower or "authentication failure" in line_lower:
            for ip in _extract_ips(line):
                ip_ssh_fail[ip] = ip_ssh_fail.get(ip, 0) + 1

        # Detect port scanning (rapid connection attempts).
        # Use word-boundary match for "syn" to avoid false positives on
        # common words like "sync", "async", "syntax", "synthesize".
        if "connection refused" in line_lower or re.search(r"\bsyn\b", line_lower):
            for ip in _extract_ips(line):
                ip_connection[ip] = ip_connection.get(ip, 0) + 1

    # Evaluate thresholds
    for ip, count in ip_401_count.items():
        if count >= _BRUTE_FORCE_THRESHOLD:
            threats.append({
                "threat_type": "http_brute_force",
                "source_ip": ip,
                "count": count,
                "description": f"IP {ip} triggered {count} HTTP 401/403 responses",
            })

    for ip, count in ip_ssh_fail.items():
        if count >= _BRUTE_FORCE_THRESHOLD:
            threats.append({
                "threat_type": "ssh_brute_force",
                "source_ip": ip,
                "count": count,
                "description": f"IP {ip} had {count} SSH authentication failures",
            })

    for ip, count in ip_connection.items():
        if count >= _PORT_SCAN_THRESHOLD:
            threats.append({
                "threat_type": "port_scan",
                "source_ip": ip,
                "count": count,
                "description": f"IP {ip} made {count} rapid connection attempts (possible port scan)",
            })

    source_ips = list({t["source_ip"] for t in threats})

    return {
        "threats_found": len(threats) > 0,
        "threat_count": len(threats),
        "threats": threats,
        "source_ips": source_ips,
        "suggested_action": (
            f"Block {len(source_ips)} source IP(s) via firewall or CrowdSec"
            if threats
            else "No threats detected"
        ),
    }


def validate_crowdsec_threat(threat: dict[str, Any]) -> tuple[str, str]:
    """Return the canonical ``(threat_type, source_ip)`` selection."""
    threat_type_value = threat.get("threat_type")
    if not isinstance(threat_type_value, str):
        raise ValueError("threat_type must be a supported string value")
    threat_type = threat_type_value.strip().lower()
    if threat_type not in ALLOWED_CROWDSEC_THREAT_TYPES:
        raise ValueError("threat_type is not supported for a CrowdSec decision")
    return threat_type, _validated_crowdsec_ip(threat.get("source_ip"))


def suggest_crowdsec_decision(threat: dict[str, Any]) -> dict[str, Any]:
    """Generate a CrowdSec-compatible decision payload for a server-detected threat.

    Args:
        threat: A single threat dict from analyze_threats().

    Returns:
        CrowdSec decision payload.
    """
    threat_type, source_ip = validate_crowdsec_threat(threat)
    description = str(threat.get("description", ""))

    duration = "24h"
    if threat_type == "ssh_brute_force":
        duration = "48h"
    elif threat_type == "port_scan":
        duration = "12h"

    return {
        "type": "ban",
        "scope": "ip",
        "value": source_ip,
        "duration": duration,
        "reason": f"InfraGuard auto-detection: {description}",
        "origin": "infraguard-ai",
        "scenario": f"infraguard/{threat_type}",
    }


def apply_crowdsec_decision(decision: dict[str, Any]) -> dict[str, Any]:
    """Apply a CrowdSec decision via the Local API.

    If CROWDSEC_API_URL is not set, operates in dry-run mode (logs only).

    Args:
        decision: CrowdSec decision payload from suggest_crowdsec_decision().

    Returns:
        Result dict with ok status and mode.
    """
    api_url = os.environ.get("CROWDSEC_API_URL", "").strip()
    api_key = os.environ.get("CROWDSEC_API_KEY", "").strip()

    if not api_url:
        logger.info("CrowdSec dry-run: would apply decision %s", decision)
        return {
            "ok": True,
            "mode": "dry-run",
            "decision": decision,
            "message": "CrowdSec not configured — decision logged but not applied",
        }

    try:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if api_key:
            headers["X-Api-Key"] = api_key

        with httpx.Client(timeout=10.0) as client:
            resp = client.post(
                f"{api_url.rstrip('/')}/v1/decisions",
                json=[decision],
                headers=headers,
            )
            resp.raise_for_status()
            return {
                "ok": True,
                "mode": "live",
                "status_code": resp.status_code,
                "decision": decision,
            }
    except httpx.HTTPError as exc:
        return {"ok": False, "error": "http_error", "message": str(exc), "decision": decision}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": "unexpected", "message": str(exc), "decision": decision}

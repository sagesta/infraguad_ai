from __future__ import annotations

import json
import os
from unittest.mock import patch

import httpx
import respx

from agent.tools.threat_response import analyze_threats, apply_crowdsec_decision, suggest_crowdsec_decision


def test_analyze_threats_empty_logs() -> None:
    result = analyze_threats([])
    assert result["threats_found"] is False
    assert result["threat_count"] == 0


def test_suggest_crowdsec_decision_structure() -> None:
    threat = {
        "threat_type": "ssh_brute_force",
        "source_ip": "192.168.1.100",
        "count": 15,
        "description": "IP 192.168.1.100 had 15 SSH authentication failures",
    }
    decision = suggest_crowdsec_decision(threat)
    assert decision["type"] == "ban"
    assert decision["scope"] == "ip"
    assert decision["value"] == "192.168.1.100"
    assert decision["duration"] == "48h"
    assert decision["origin"] == "infraguard-ai"


def test_apply_crowdsec_decision_dry_run() -> None:
    decision = {
        "type": "ban",
        "scope": "ip",
        "value": "192.168.1.100",
        "duration": "48h",
        "reason": "Test",
        "origin": "test",
        "scenario": "test",
    }
    with patch.dict(os.environ, {"CROWDSEC_API_URL": ""}, clear=True):
        result = apply_crowdsec_decision(decision)
        assert result["ok"] is True
        assert result["mode"] == "dry-run"
        assert result["decision"] == decision


def test_apply_crowdsec_decision_requires_machine_credentials() -> None:
    decision = suggest_crowdsec_decision(
        {
            "threat_type": "http_brute_force",
            "source_ip": "203.0.113.10",
            "description": "repeated login failures",
        }
    )
    with patch.dict(
        os.environ,
        {"CROWDSEC_API_URL": "http://devplanner-crowdsec:8080"},
        clear=True,
    ):
        result = apply_crowdsec_decision(decision)

    assert result["ok"] is False
    assert result["error"] == "configuration"


@respx.mock
def test_apply_crowdsec_decision_uses_machine_jwt() -> None:
    api_url = "http://devplanner-crowdsec:8080"
    decision = suggest_crowdsec_decision(
        {
            "threat_type": "http_brute_force",
            "source_ip": "203.0.113.10",
            "description": "repeated login failures",
        }
    )
    login_route = respx.post(f"{api_url}/v1/watchers/login").mock(
        return_value=httpx.Response(200, json={"token": "machine-jwt"})
    )
    decision_route = respx.post(f"{api_url}/v1/decisions").mock(
        return_value=httpx.Response(201)
    )

    with patch.dict(
        os.environ,
        {
            "CROWDSEC_API_URL": api_url,
            "CROWDSEC_MACHINE_ID": "infraguard",
            "CROWDSEC_MACHINE_PASSWORD": "test-password",
        },
        clear=True,
    ):
        result = apply_crowdsec_decision(decision)

    assert result["ok"] is True
    assert result["mode"] == "live"
    assert login_route.called
    assert decision_route.called
    request = decision_route.calls.last.request
    assert request.headers["Authorization"] == "Bearer machine-jwt"
    assert json.loads(request.content) == [decision]

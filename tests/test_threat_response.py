from __future__ import annotations

import os
from unittest.mock import patch

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
    with patch.dict(os.environ, {"CROWDSEC_API_URL": ""}):
        result = apply_crowdsec_decision(decision)
        assert result["ok"] is True
        assert result["mode"] == "dry-run"
        assert result["decision"] == decision

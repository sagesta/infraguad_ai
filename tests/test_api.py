from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health() -> None:
    with patch("api.main.store.fetch_last_check_iso", new_callable=AsyncMock) as mock_last_check:
        mock_last_check.return_value = "2026-04-26T10:00:00+00:00"
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


def test_login_returns_200() -> None:
    response = client.get("/login")
    assert response.status_code == 200


def test_status_redirects_to_login_without_auth() -> None:
    # Explicitly disabling automatic redirects in TestClient
    response = client.get("/status", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/login"


def test_threats_api_returns_valid_json() -> None:
    with patch("api.main.store.fetch_latest_verdict", new_callable=AsyncMock) as mock_verdict:
        mock_verdict.return_value = None
        with patch("agent.tools.threat_response.analyze_threats") as mock_analyze:
            mock_analyze.return_value = {
                "threats_found": False,
                "threat_count": 0,
                "threats": [],
                "source_ips": [],
                "suggested_action": "No threats detected",
            }
            # We need to simulate an authenticated request to get past AuthMiddleware
            # We can mock validate_session_token to always succeed
            with patch("api.main.validate_session_token") as mock_validate:
                mock_validate.return_value = {"sub": "admin"}
                response = client.get("/api/threats", cookies={"session": "fake-session"})
                assert response.status_code == 200
                data = response.json()
                assert "threats_found" in data
                assert data["threats_found"] is False

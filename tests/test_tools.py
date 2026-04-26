"""HTTP tool tests with mocked upstreams (pytest + respx)."""

from __future__ import annotations

import asyncio
import os
import re
from unittest.mock import MagicMock, patch

import httpx
import respx

from agent.tools.docker_logs import fetch_container_errors
from agent.tools.http_probe import probe_endpoints
from agent.tools.loki import fetch_loki_logs
from agent.tools.prometheus import query_prometheus


@respx.mock
def test_fetch_loki_logs_parses_streams() -> None:
    os.environ["LOKI_URL"] = "http://loki.test"
    payload = {
        "status": "success",
        "data": {
            "resultType": "streams",
            "result": [
                {
                    "stream": {"job": "api"},
                    "values": [
                        ["1700000000000000000", "line-one"],
                        ["1700000000000000001", "line-two"],
                    ],
                }
            ],
        },
    }
    respx.get("http://loki.test/loki/api/v1/query").mock(
        return_value=httpx.Response(200, json=payload)
    )

    out = fetch_loki_logs()
    assert out["ok"] is True
    assert out["count"] == 2
    lines = out["lines"]
    assert lines[0]["line"] == "line-one"


@respx.mock
def test_query_prometheus_collects_metrics() -> None:
    os.environ["PROMETHEUS_URL"] = "http://prom.test"
    respx.get(re.compile(r"http://prom\.test/api/v1/query\?.*")).mock(
        return_value=httpx.Response(
            200,
            json={"status": "success", "data": {"resultType": "vector", "result": [{"metric": {}, "value": [1, "2"]}]}},
        )
    )

    out = query_prometheus()
    assert out["ok"] is True
    metrics = out["metrics"]
    for key in ("cpu_busy_ratio", "memory_available_ratio", "disk_avail_bytes_root", "http_5xx_ratio"):
        assert key in metrics
        assert metrics[key]["ok"] is True


@respx.mock
def test_probe_endpoints_records_latency() -> None:
    os.environ["PROBE_URLS"] = "http://svc/health,http://svc/"
    respx.get("http://svc/health").mock(return_value=httpx.Response(200, text="ok"))
    respx.get("http://svc/").mock(return_value=httpx.Response(500, text="boom"))

    out = probe_endpoints()
    assert out["ok"] is True
    probes = out["probes"]
    assert probes[0]["status_code"] == 200
    assert probes[1]["status_code"] == 500


def test_loki_missing_env_returns_none() -> None:
    os.environ.pop("LOKI_URL", None)
    out = fetch_loki_logs()
    assert out is None


@patch("agent.tools.docker_logs.docker.from_env")
def test_fetch_container_errors_filters_keywords(mock_from_env: MagicMock) -> None:
    client = MagicMock()
    mock_from_env.return_value = client
    container = MagicMock()
    container.logs.return_value = (
        b"2020-01-01T00:00:00.000000000Z info: ok\n"
        b"2020-01-01T00:00:01.000000000Z Error: database failed\n"
        b"2020-01-01T00:00:02.000000000Z another line\n"
    )
    client.containers.get.return_value = container

    out = asyncio.run(fetch_container_errors("svc", tail=100))
    assert len(out) == 1
    assert out[0]["timestamp"] == "2020-01-01T00:00:01.000000000Z"
    assert "Error: database failed" in out[0]["line"]
    client.close.assert_called_once()


@patch("agent.tools.docker_logs.docker.from_env", side_effect=Exception("no socket"))
def test_fetch_container_errors_swallows_docker_init(mock_from_env: MagicMock) -> None:
    out = asyncio.run(fetch_container_errors("any"))
    assert out == []


@patch("agent.tools.docker_logs.docker.from_env")
def test_fetch_container_errors_not_found(mock_from_env: MagicMock) -> None:
    from docker.errors import NotFound

    client = MagicMock()
    mock_from_env.return_value = client
    client.containers.get.side_effect = NotFound("nope")

    out = asyncio.run(fetch_container_errors("missing"))
    assert out == []
    client.close.assert_called_once()


def test_fetch_container_errors_empty_name() -> None:
    out = asyncio.run(fetch_container_errors("  \t  "))
    assert out == []

"""HTTP tool tests with mocked upstreams (pytest + respx)."""

from __future__ import annotations

import asyncio
import os
import re

import httpx
import respx

from agent.tools.app_errors import fetch_app_errors
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


def test_loki_missing_env_returns_error_dict() -> None:
    os.environ.pop("LOKI_URL", None)
    out = fetch_loki_logs()
    assert out["ok"] is False
    assert out["error"] == "missing_env"


@respx.mock
def test_fetch_app_errors_parses_json_list() -> None:
    os.environ["DEVPLANNER_API_URL"] = "http://devplanner-api:3000"
    respx.get(re.compile(r"http://devplanner-api:3000/errors/recent\?limit=50")).mock(
        return_value=httpx.Response(200, json=[{"message": "boom"}])
    )
    out = asyncio.run(fetch_app_errors())
    assert out["ok"] is True
    assert out["count"] == 1
    assert out["errors"][0]["message"] == "boom"


@respx.mock
def test_fetch_app_errors_parses_errors_key() -> None:
    os.environ["DEVPLANNER_API_URL"] = "http://api.test"
    respx.get(re.compile(r"http://api\.test/errors/recent\?limit=50")).mock(
        return_value=httpx.Response(200, json={"errors": [{"code": "E1"}]})
    )
    out = asyncio.run(fetch_app_errors())
    assert out["ok"] is True
    assert len(out["errors"]) == 1
    assert out["errors"][0]["code"] == "E1"


def test_fetch_app_errors_missing_env() -> None:
    os.environ.pop("DEVPLANNER_API_URL", None)
    out = asyncio.run(fetch_app_errors())
    assert out["ok"] is False
    assert out["error"] == "missing_env"

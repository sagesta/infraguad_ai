"""FastAPI service: status, alerts, health, and dashboard."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from api import store


def _load_env() -> None:
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_env()
    await store.init_db()
    yield


app = FastAPI(title="InfraGuard AI API", lifespan=lifespan)


@app.get("/status")
async def get_status() -> JSONResponse:
    latest = await store.fetch_latest_verdict()
    if not latest:
        return JSONResponse({"verdict": None})
    payload = latest.get("payload") or {}
    verdict = payload.get("verdict") if isinstance(payload, dict) else None
    return JSONResponse(
        {
            "created_at": latest.get("created_at"),
            "severity": latest.get("severity"),
            "summary": latest.get("summary"),
            "verdict": verdict,
            "extras": payload.get("extras") if isinstance(payload, dict) else None,
        }
    )


@app.get("/alerts")
async def get_alerts() -> JSONResponse:
    rows = await store.fetch_recent_verdicts(20)
    alerts: list[dict[str, Any]] = []
    for row in rows:
        alerts.append(
            {
                "id": row.get("id"),
                "created_at": row.get("created_at"),
                "severity": row.get("severity"),
                "summary": row.get("summary"),
            }
        )
    return JSONResponse({"alerts": alerts})


@app.get("/health")
async def health() -> JSONResponse:
    last = await store.fetch_last_check_iso()
    agent = "unknown"
    if last:
        ts = datetime.fromisoformat(last)
        age = (datetime.now(timezone.utc) - ts).total_seconds()
        agent = "running" if age <= 120 else "stale"
    return JSONResponse({"status": "ok", "agent": agent, "last_check": last})


@app.get("/")
async def dashboard() -> FileResponse:
    root = Path(__file__).resolve().parents[1]
    path = root / "dashboard" / "index.html"
    return FileResponse(path)


def create_app() -> FastAPI:
    return app

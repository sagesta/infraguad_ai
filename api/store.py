"""SQLite persistence for LLM verdicts (shared between agent and API)."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

import aiosqlite


def _db_path() -> str:
    return os.environ.get("DB_PATH", "./data/verdicts.db")


SCHEMA = """
CREATE TABLE IF NOT EXISTS verdicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    severity TEXT NOT NULL,
    summary TEXT NOT NULL,
    payload TEXT NOT NULL
);
"""


async def init_db() -> None:
    path = _db_path()
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    async with aiosqlite.connect(path) as db:
        await db.execute(SCHEMA)
        await db.commit()


async def insert_verdict(verdict: dict[str, Any], extras: dict[str, Any] | None = None) -> int:
    """Persist a verdict row; returns inserted id."""
    payload = {"verdict": verdict}
    if extras:
        payload["extras"] = extras
    created = datetime.now(timezone.utc).isoformat()
    severity = str(verdict.get("severity", "ok"))
    summary = str(verdict.get("summary", ""))
    body = json.dumps(payload, default=str)

    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(SCHEMA)
        cur = await db.execute(
            "INSERT INTO verdicts (created_at, severity, summary, payload) VALUES (?, ?, ?, ?)",
            (created, severity, summary, body),
        )
        await db.commit()
        return int(cur.lastrowid or 0)


async def fetch_latest_verdict() -> dict[str, Any] | None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(SCHEMA)
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, created_at, severity, summary, payload FROM verdicts ORDER BY id DESC LIMIT 1"
        )
        row = await cur.fetchone()
        if not row:
            return None
        data = dict(row)
        data["payload"] = json.loads(data["payload"])
        return data


async def fetch_recent_verdicts(limit: int = 20) -> list[dict[str, Any]]:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(SCHEMA)
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT id, created_at, severity, summary, payload
            FROM verdicts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = await cur.fetchall()
        out: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["payload"] = json.loads(item["payload"])
            out.append(item)
        return out


async def fetch_last_check_iso() -> str | None:
    async with aiosqlite.connect(_db_path()) as db:
        await db.execute(SCHEMA)
        cur = await db.execute("SELECT created_at FROM verdicts ORDER BY id DESC LIMIT 1")
        row = await cur.fetchone()
        if not row:
            return None
        return str(row[0])

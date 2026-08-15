"""SQLite persistence for LLM verdicts and acknowledgements (shared between agent and API)."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import aiosqlite

from agent.llm.providers import active_model
from agent.memory import compute_fingerprint, derive_signature_fallback


def _db_path() -> str:
    return os.environ.get("DB_PATH", "./data/verdicts.db")


def _retention_days() -> int:
    raw = os.environ.get("VERDICT_RETENTION_DAYS", "").strip() or "30"
    try:
        return max(int(raw), 1)
    except ValueError:
        return 30


def _ack_ttl_days() -> int:
    """Acknowledgement lifetime in days; <= 0 means no expiry."""
    raw = os.environ.get("ACK_TTL_DAYS", "").strip() or "30"
    try:
        return int(raw)
    except ValueError:
        return 30


VERDICTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS verdicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    severity TEXT NOT NULL,
    summary TEXT NOT NULL,
    payload TEXT NOT NULL,
    signature TEXT,
    fingerprint TEXT
);
"""

ACKS_SCHEMA = """
CREATE TABLE IF NOT EXISTS acknowledgements (
    fingerprint TEXT PRIMARY KEY,
    signature TEXT,
    severity TEXT,
    summary TEXT,
    note TEXT,
    acked_by TEXT,
    created_at TEXT NOT NULL,
    expires_at TEXT
);
"""

# Back-compat alias: existing callers/tests import SCHEMA for the verdicts table.
SCHEMA = VERDICTS_SCHEMA


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_suppressed(severity: str, acknowledged: bool) -> bool:
    """An acknowledged condition is hidden only when low-risk.

    high/critical always surface, acknowledged or not.
    """
    return acknowledged and str(severity or "").lower() in {"ok", "warning"}


async def _ensure_schema(db: aiosqlite.Connection) -> None:
    await db.execute(VERDICTS_SCHEMA)
    await db.execute(ACKS_SCHEMA)
    # Migrate pre-existing verdicts tables that lack the memory columns.
    cur = await db.execute("PRAGMA table_info(verdicts)")
    cols = {row[1] for row in await cur.fetchall()}
    if "signature" not in cols:
        await db.execute("ALTER TABLE verdicts ADD COLUMN signature TEXT")
    if "fingerprint" not in cols:
        await db.execute("ALTER TABLE verdicts ADD COLUMN fingerprint TEXT")
    # Fingerprint is the lookup key for fetch_verdict_by_fingerprint and ack joins.
    await db.execute("CREATE INDEX IF NOT EXISTS idx_verdicts_fingerprint ON verdicts(fingerprint)")


async def init_db() -> None:
    path = _db_path()
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    async with aiosqlite.connect(path) as db:
        await _ensure_schema(db)
        await db.commit()


async def insert_verdict(verdict: dict[str, Any], extras: dict[str, Any] | None = None) -> int:
    """Persist a verdict row (with its memory fingerprint); returns inserted id."""
    payload = {"verdict": verdict}
    if extras:
        payload["extras"] = extras
    created = _now_iso()
    severity = str(verdict.get("severity", "ok"))
    summary = str(verdict.get("summary", ""))
    body = json.dumps(payload, default=str)

    signature = str(verdict.get("signature") or "").strip()
    if not signature:
        signature = derive_signature_fallback(severity, str(verdict.get("root_cause", "")), summary)
    # The active provider's model is part of the fingerprint, so switching
    # provider/model re-opens previously acknowledged conditions by design.
    fingerprint = compute_fingerprint(signature, model=active_model())

    cutoff = (datetime.now(timezone.utc) - timedelta(days=_retention_days())).isoformat()

    async with aiosqlite.connect(_db_path()) as db:
        await _ensure_schema(db)
        cur = await db.execute(
            "INSERT INTO verdicts (created_at, severity, summary, payload, signature, fingerprint) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (created, severity, summary, body, signature, fingerprint),
        )
        # created_at is UTC ISO-8601, so string comparison orders chronologically.
        await db.execute("DELETE FROM verdicts WHERE created_at < ?", (cutoff,))
        await db.commit()
        return int(cur.lastrowid or 0)


async def _active_ack_fingerprints(db: aiosqlite.Connection) -> set[str]:
    cur = await db.execute(
        "SELECT fingerprint FROM acknowledgements WHERE expires_at IS NULL OR expires_at > ?",
        (_now_iso(),),
    )
    return {row[0] for row in await cur.fetchall()}


def _annotate(item: dict[str, Any], acked: set[str]) -> dict[str, Any]:
    fp = item.get("fingerprint")
    item["acknowledged"] = bool(fp and fp in acked)
    item["suppressed"] = is_suppressed(item.get("severity", ""), item["acknowledged"])
    return item


async def fetch_latest_verdict() -> dict[str, Any] | None:
    async with aiosqlite.connect(_db_path()) as db:
        await _ensure_schema(db)
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, created_at, severity, summary, payload, signature, fingerprint "
            "FROM verdicts ORDER BY id DESC LIMIT 1"
        )
        row = await cur.fetchone()
        if not row:
            return None
        acked = await _active_ack_fingerprints(db)
        data = dict(row)
        data["payload"] = json.loads(data["payload"])
        return _annotate(data, acked)


async def fetch_recent_verdicts(limit: int = 20) -> list[dict[str, Any]]:
    async with aiosqlite.connect(_db_path()) as db:
        await _ensure_schema(db)
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, created_at, severity, summary, payload, signature, fingerprint "
            "FROM verdicts ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = await cur.fetchall()
        acked = await _active_ack_fingerprints(db)
        out: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["payload"] = json.loads(item["payload"])
            out.append(_annotate(item, acked))
        return out


async def fetch_verdict_by_fingerprint(fingerprint: str) -> dict[str, Any] | None:
    """Most recent verdict carrying this fingerprint (used when acknowledging)."""
    async with aiosqlite.connect(_db_path()) as db:
        await _ensure_schema(db)
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, created_at, severity, summary, signature, fingerprint "
            "FROM verdicts WHERE fingerprint = ? ORDER BY id DESC LIMIT 1",
            (fingerprint,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None


async def insert_ack(
    fingerprint: str,
    *,
    signature: str = "",
    severity: str = "",
    summary: str = "",
    note: str = "",
    acked_by: str = "operator",
) -> dict[str, Any]:
    """Record (or refresh) an acknowledgement for a fingerprint.

    Expires after ACK_TTL_DAYS (default 30; <= 0 disables expiry) as a backstop
    so nothing is suppressed forever.
    """
    created = _now_iso()
    ttl = _ack_ttl_days()
    expires_at = (
        (datetime.now(timezone.utc) + timedelta(days=ttl)).isoformat() if ttl > 0 else None
    )
    async with aiosqlite.connect(_db_path()) as db:
        await _ensure_schema(db)
        await db.execute(
            "INSERT OR REPLACE INTO acknowledgements "
            "(fingerprint, signature, severity, summary, note, acked_by, created_at, expires_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (fingerprint, signature, severity, summary, note, acked_by, created, expires_at),
        )
        await db.commit()
    return {"fingerprint": fingerprint, "created_at": created, "expires_at": expires_at}


async def delete_ack(fingerprint: str) -> None:
    async with aiosqlite.connect(_db_path()) as db:
        await _ensure_schema(db)
        await db.execute("DELETE FROM acknowledgements WHERE fingerprint = ?", (fingerprint,))
        await db.commit()


async def fetch_active_acks() -> list[dict[str, Any]]:
    """Non-expired acknowledgements, newest first (fed into the agent prompt)."""
    async with aiosqlite.connect(_db_path()) as db:
        await _ensure_schema(db)
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT fingerprint, signature, severity, summary, note, acked_by, created_at, expires_at "
            "FROM acknowledgements WHERE expires_at IS NULL OR expires_at > ? "
            "ORDER BY created_at DESC",
            (_now_iso(),),
        )
        return [dict(row) for row in await cur.fetchall()]

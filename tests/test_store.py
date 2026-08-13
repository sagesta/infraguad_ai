"""SQLite store tests: retention pruning and round-trips."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import aiosqlite
import pytest

from agent.memory import compute_fingerprint
from api import store


async def _insert_raw_row(db_path: str, created_at: str) -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.execute(store.SCHEMA)
        await db.execute(
            "INSERT INTO verdicts (created_at, severity, summary, payload) VALUES (?, ?, ?, ?)",
            (created_at, "ok", "old row", "{}"),
        )
        await db.commit()


async def test_insert_verdict_prunes_expired_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db_path = str(tmp_path / "verdicts.db")
    monkeypatch.setenv("DB_PATH", db_path)
    monkeypatch.setenv("VERDICT_RETENTION_DAYS", "30")

    await store.init_db()
    expired = (datetime.now(timezone.utc) - timedelta(days=45)).isoformat()
    await _insert_raw_row(db_path, expired)

    await store.insert_verdict({"severity": "ok", "summary": "fresh row"})

    rows = await store.fetch_recent_verdicts(50)
    assert len(rows) == 1
    assert rows[0]["summary"] == "fresh row"


async def test_insert_verdict_keeps_rows_within_retention(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db_path = str(tmp_path / "verdicts.db")
    monkeypatch.setenv("DB_PATH", db_path)
    monkeypatch.setenv("VERDICT_RETENTION_DAYS", "30")

    await store.init_db()
    recent = (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
    await _insert_raw_row(db_path, recent)

    await store.insert_verdict({"severity": "warning", "summary": "fresh row"})

    rows = await store.fetch_recent_verdicts(50)
    assert len(rows) == 2


async def test_fetch_latest_verdict_round_trip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db_path = str(tmp_path / "verdicts.db")
    monkeypatch.setenv("DB_PATH", db_path)

    await store.init_db()
    verdict = {
        "severity": "high",
        "summary": "Disk almost full",
        "root_cause": "Log growth",
        "recommended_action": "Rotate logs",
    }
    await store.insert_verdict(verdict, extras={"llm_mode": "gemini_direct"})

    latest = await store.fetch_latest_verdict()
    assert latest is not None
    assert latest["severity"] == "high"
    assert latest["payload"]["verdict"]["summary"] == "Disk almost full"
    assert latest["payload"]["extras"]["llm_mode"] == "gemini_direct"


# --- Verdict memory: fingerprints and acknowledgements ---


async def test_insert_verdict_stores_signature_and_fingerprint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "verdicts.db"))
    await store.init_db()
    await store.insert_verdict(
        {"severity": "warning", "summary": "Disk low", "root_cause": "x", "signature": "prometheus:disk-low:/"}
    )
    latest = await store.fetch_latest_verdict()
    assert latest["signature"] == "prometheus:disk-low:/"
    assert latest["fingerprint"] == compute_fingerprint("prometheus:disk-low:/")
    assert latest["acknowledged"] is False
    assert latest["suppressed"] is False


async def test_acknowledge_suppresses_warning_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "verdicts.db"))
    await store.init_db()
    await store.insert_verdict({"severity": "warning", "summary": "Disk low", "signature": "prometheus:disk-low:/"})
    fp = compute_fingerprint("prometheus:disk-low:/")
    await store.insert_ack(fp, signature="prometheus:disk-low:/", severity="warning", summary="Disk low")

    latest = await store.fetch_latest_verdict()
    assert latest["acknowledged"] is True
    assert latest["suppressed"] is True


async def test_is_suppressed_never_hides_critical() -> None:
    assert store.is_suppressed("warning", True) is True
    assert store.is_suppressed("ok", True) is True
    assert store.is_suppressed("high", True) is False
    assert store.is_suppressed("critical", True) is False
    assert store.is_suppressed("warning", False) is False


async def test_expired_ack_is_not_active(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db_path = str(tmp_path / "verdicts.db")
    monkeypatch.setenv("DB_PATH", db_path)
    await store.init_db()
    await store.insert_verdict({"severity": "warning", "summary": "x", "signature": "a:b:c"})
    fp = compute_fingerprint("a:b:c")

    past = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "INSERT OR REPLACE INTO acknowledgements (fingerprint, created_at, expires_at) VALUES (?, ?, ?)",
            (fp, past, past),
        )
        await db.commit()

    assert all(a["fingerprint"] != fp for a in await store.fetch_active_acks())
    latest = await store.fetch_latest_verdict()
    assert latest["acknowledged"] is False


async def test_delete_ack_reopens_condition(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "verdicts.db"))
    await store.init_db()
    await store.insert_verdict({"severity": "warning", "summary": "S", "signature": "a:b:c"})
    fp = compute_fingerprint("a:b:c")
    await store.insert_ack(fp)
    assert (await store.fetch_latest_verdict())["acknowledged"] is True
    await store.delete_ack(fp)
    assert (await store.fetch_latest_verdict())["acknowledged"] is False


async def test_fetch_verdict_by_fingerprint(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "verdicts.db"))
    await store.init_db()
    await store.insert_verdict({"severity": "warning", "summary": "S", "signature": "a:b:c"})
    fp = compute_fingerprint("a:b:c")
    row = await store.fetch_verdict_by_fingerprint(fp)
    assert row is not None and row["summary"] == "S"
    assert await store.fetch_verdict_by_fingerprint("nope") is None

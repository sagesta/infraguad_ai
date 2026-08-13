from __future__ import annotations

import os
from unittest.mock import patch

from langchain_core.documents import Document

from agent.rag.local_runbooks_loader import load_local_runbooks, runbooks_configured
from agent.rag.runbook_agent import query_runbooks


# --- local_runbooks_loader ---


def test_load_local_runbooks_reads_markdown_files(tmp_path, monkeypatch) -> None:
    (tmp_path / "deployment").mkdir()
    (tmp_path / "deployment" / "rollback.md").write_text(
        "# Rollback a bad deploy\n\nRevert the image tag and redeploy.", encoding="utf-8"
    )
    (tmp_path / "disk-full.md").write_text("Prune old logs under /var/log.", encoding="utf-8")

    monkeypatch.setenv("RUNBOOKS_DIR", str(tmp_path))
    docs = load_local_runbooks()

    assert len(docs) == 2
    titles = {doc.metadata["title"] for doc in docs}
    assert "Rollback a bad deploy" in titles  # from the markdown heading
    assert "Disk Full" in titles  # derived from the filename, no heading present

    rollback = next(d for d in docs if d.metadata["title"] == "Rollback a bad deploy")
    assert rollback.metadata["category"] == "deployment"


def test_load_local_runbooks_missing_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("RUNBOOKS_DIR", str(tmp_path / "does-not-exist"))
    assert load_local_runbooks() == []


def test_load_local_runbooks_empty_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("RUNBOOKS_DIR", str(tmp_path))
    assert load_local_runbooks() == []


def test_runbooks_configured(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("RUNBOOKS_DIR", str(tmp_path))
    assert runbooks_configured() is False
    (tmp_path / "one.md").write_text("content", encoding="utf-8")
    assert runbooks_configured() is True


# --- runbook_agent.query_runbooks ---


def test_query_runbooks_no_documents_indexed() -> None:
    with patch("agent.rag.runbook_agent.similarity_search", return_value=[]):
        result = query_runbooks("What is the runbook for database failover?")
    assert result["ok"] is True
    assert result["sources"] == []
    assert "index" in result["answer"].lower()


def test_query_runbooks_answers_from_retrieved_docs(monkeypatch) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    doc = Document(page_content="Restart the primary, then promote the replica.", metadata={"title": "Failover", "source": "file://failover.md"})

    class _FakeChain:
        def __or__(self, other):
            return self

        def invoke(self, _inputs):
            return "Promote the replica after confirming primary is down."

    fake_llm = object()
    with patch("agent.rag.runbook_agent.similarity_search", return_value=[doc]), \
         patch("agent.rag.runbook_agent.build_chat_model", return_value=fake_llm), \
         patch("agent.rag.runbook_agent._RAG_PROMPT", _FakeChain()):
        result = query_runbooks("How do I fail over the database?")

    assert result["ok"] is True
    assert result["sources"] == [{"title": "Failover", "source": "file://failover.md"}]


def test_query_runbooks_propagates_provider_error(monkeypatch) -> None:
    doc = Document(page_content="x", metadata={"title": "T"})
    error = {"ok": False, "error": "missing_env", "message": "OLLAMA_BASE_URL unreachable"}
    with patch("agent.rag.runbook_agent.similarity_search", return_value=[doc]), \
         patch("agent.rag.runbook_agent.build_chat_model", return_value=error):
        result = query_runbooks("question")
    assert result == error

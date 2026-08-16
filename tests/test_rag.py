from __future__ import annotations

import os
from unittest.mock import patch

import numpy as np
from langchain_core.documents import Document

from agent.rag.local_runbooks_loader import load_local_runbooks, runbooks_configured
from agent.rag.runbook_agent import query_runbooks
from agent.rag.vector_store import _LocalEmbeddings


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


def test_local_embeddings_return_native_python_floats() -> None:
    embeddings = object.__new__(_LocalEmbeddings)
    embeddings._fn = lambda texts: np.array(
        [[0.25, -0.5] for _ in texts],
        dtype=np.float32,
    )

    document_vectors = embeddings.embed_documents(["first", "second"])
    query_vector = embeddings.embed_query("question")

    assert all(type(value) is float for vector in document_vectors for value in vector)
    assert all(type(value) is float for value in query_vector)


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

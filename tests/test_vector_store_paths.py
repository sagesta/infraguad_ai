"""Lifecycle and failure-path tests for the local Chroma runbook index."""

from __future__ import annotations

from unittest.mock import MagicMock, sentinel

import pytest
from langchain_core.documents import Document

from agent.rag import vector_store


def test_local_embeddings_initialises_chroma_default_without_downloading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import chromadb.utils.embedding_functions as embedding_functions

    embedder = MagicMock(return_value=[[0.1, 0.2]])
    constructor = MagicMock(return_value=embedder)
    monkeypatch.setattr(embedding_functions, "DefaultEmbeddingFunction", constructor)

    embeddings = vector_store._LocalEmbeddings()

    constructor.assert_called_once_with()
    assert embeddings._fn is embedder


def test_local_embeddings_normalises_scalar_values_to_builtin_float() -> None:
    embeddings = object.__new__(vector_store._LocalEmbeddings)
    embeddings._fn = lambda texts: [[index + 0.25, index + 0.5] for index, _ in enumerate(texts)]

    document_vectors = embeddings.embed_documents(["first", "second"])
    query_vector = embeddings.embed_query("question")

    assert document_vectors == [[0.25, 0.5], [1.25, 1.5]]
    assert query_vector == [0.25, 0.5]
    assert all(type(value) is float for row in document_vectors for value in row)
    assert all(type(value) is float for value in query_vector)


def test_get_embedding_function_constructs_local_adapter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    constructor = MagicMock(return_value=sentinel.embeddings)
    monkeypatch.setattr(vector_store, "_LocalEmbeddings", constructor)

    assert vector_store._get_embedding_function() is sentinel.embeddings
    constructor.assert_called_once_with()


def test_build_index_empty_input_clears_existing_records(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    from langchain_community import vectorstores

    store = MagicMock()
    store.get.return_value = {"ids": ["old-runbook-id"]}
    monkeypatch.setattr(vector_store, "_CHROMA_DIR", str(tmp_path / "index"))
    monkeypatch.setattr(vector_store, "_get_embedding_function", lambda: sentinel.embeddings)
    constructor = MagicMock(return_value=store)
    monkeypatch.setattr(vectorstores, "Chroma", constructor)

    assert vector_store.build_index([]) == 0
    constructor.assert_called_once_with(
        persist_directory=str((tmp_path / "index").resolve()),
        embedding_function=sentinel.embeddings,
        collection_name="runbooks",
    )
    store.add_documents.assert_not_called()
    store.delete.assert_called_once_with(ids=["old-runbook-id"])
    assert "clearing the existing runbook index" in caplog.text


def test_build_index_reindexes_without_duplicates_or_stale_records(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    from langchain_community import vectorstores

    first_documents = [
        Document(
            page_content="Restart the database",
            metadata={"source": "file://db.md", "chunk_id": 0},
        ),
        Document(page_content="Check disk capacity", metadata={"source": "file://disk.md"}),
        Document(page_content="Inspect the network", metadata={"source": "file://network.md"}),
    ]
    second_documents = [
        Document(
            page_content="Restart the database, then verify replication",
            metadata={"source": "file://db.md", "chunk_id": 0},
        ),
        Document(page_content="Inspect the network", metadata={"source": "file://network.md"}),
    ]

    class _InMemoryChroma:
        records: dict[str, Document] = {}
        init_calls: list[dict] = []

        def __init__(self, **kwargs) -> None:
            self.init_calls.append(kwargs)

        def get(self, *, include) -> dict[str, list[str]]:
            assert include == []
            return {"ids": list(self.records)}

        def add_documents(self, *, documents, ids) -> None:
            for document, document_id in zip(documents, ids, strict=True):
                self.records[document_id] = document

        def delete(self, *, ids) -> None:
            for document_id in ids:
                self.records.pop(document_id)

    _InMemoryChroma.records = {}
    monkeypatch.setattr(vector_store, "_CHROMA_DIR", str(tmp_path / "index"))
    monkeypatch.setattr(vector_store, "_get_embedding_function", lambda: sentinel.embeddings)
    monkeypatch.setattr(vectorstores, "Chroma", _InMemoryChroma)

    assert vector_store.build_index(first_documents) == 3
    first_ids = set(_InMemoryChroma.records)
    assert vector_store.build_index(second_documents) == 2

    assert len(_InMemoryChroma.records) == 2
    assert first_ids.intersection(_InMemoryChroma.records) == set(_InMemoryChroma.records)
    assert len(_InMemoryChroma.init_calls) == 2
    assert all(
        call == {
            "persist_directory": str((tmp_path / "index").resolve()),
            "embedding_function": sentinel.embeddings,
            "collection_name": "runbooks",
        }
        for call in _InMemoryChroma.init_calls
    )
    assert {document.metadata["source"] for document in _InMemoryChroma.records.values()} == {
        "file://db.md",
        "file://network.md",
    }
    assert any(
        document.page_content.endswith("verify replication")
        for document in _InMemoryChroma.records.values()
    )


def test_build_index_raises_distinct_error_when_chroma_fails(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    from langchain_community import vectorstores

    monkeypatch.setattr(vector_store, "_get_embedding_function", lambda: sentinel.embeddings)
    store = MagicMock()
    store.get.return_value = {"ids": ["previous-id"]}
    store.add_documents.side_effect = RuntimeError("index locked")
    monkeypatch.setattr(vectorstores, "Chroma", MagicMock(return_value=store))

    with pytest.raises(vector_store.VectorIndexBuildError) as exc_info:
        vector_store.build_index([Document(page_content="runbook")])

    assert isinstance(exc_info.value.__cause__, RuntimeError)
    store.delete.assert_not_called()
    assert "index locked" in caplog.text

    store.get.return_value = {"ids": []}
    store.add_documents.side_effect = None
    duplicate_source = [
        Document(page_content="first", metadata={"source": "file://same.md"}),
        Document(page_content="second", metadata={"source": "file://same.md"}),
    ]
    with pytest.raises(vector_store.VectorIndexBuildError) as duplicate_error:
        vector_store.build_index(duplicate_source)
    assert isinstance(duplicate_error.value.__cause__, ValueError)
    assert "duplicate source identities" in str(duplicate_error.value.__cause__)


def test_load_index_returns_none_when_directory_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(vector_store, "_CHROMA_DIR", str(tmp_path / "missing"))

    assert vector_store.load_index() is None


def test_load_index_constructs_existing_collection(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    from langchain_community import vectorstores

    index_dir = tmp_path / "index"
    index_dir.mkdir()
    monkeypatch.setattr(vector_store, "_CHROMA_DIR", str(index_dir))
    monkeypatch.setattr(vector_store, "_get_embedding_function", lambda: sentinel.embeddings)
    constructor = MagicMock(return_value=sentinel.store)
    monkeypatch.setattr(vectorstores, "Chroma", constructor)

    assert vector_store.load_index() is sentinel.store
    constructor.assert_called_once_with(
        persist_directory=str(index_dir.resolve()),
        embedding_function=sentinel.embeddings,
        collection_name="runbooks",
    )


def test_load_index_returns_none_when_chroma_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    from langchain_community import vectorstores

    index_dir = tmp_path / "index"
    index_dir.mkdir()
    monkeypatch.setattr(vector_store, "_CHROMA_DIR", str(index_dir))
    monkeypatch.setattr(vector_store, "_get_embedding_function", lambda: sentinel.embeddings)
    monkeypatch.setattr(vectorstores, "Chroma", MagicMock(side_effect=RuntimeError("corrupt index")))

    assert vector_store.load_index() is None
    assert "corrupt index" in caplog.text


def test_similarity_search_returns_empty_when_index_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(vector_store, "load_index", lambda: None)

    assert vector_store.similarity_search("database failover") == []


def test_similarity_search_delegates_query_and_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = [Document(page_content="Promote the replica")]
    store = MagicMock()
    store.similarity_search.return_value = expected
    monkeypatch.setattr(vector_store, "load_index", lambda: store)

    assert vector_store.similarity_search("database failover", k=7) == expected
    store.similarity_search.assert_called_once_with("database failover", k=7)


def test_similarity_search_contains_store_error(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    store = MagicMock()
    store.similarity_search.side_effect = RuntimeError("query failed")
    monkeypatch.setattr(vector_store, "load_index", lambda: store)

    assert vector_store.similarity_search("database failover") == []
    assert "query failed" in caplog.text

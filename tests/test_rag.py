from __future__ import annotations

import os
from unittest.mock import patch

from agent.rag.runbook_agent import query_runbooks


def test_query_runbooks_structure() -> None:
    with patch.dict(os.environ, {"GCP_PROJECT_ID": "test-project", "NOTION_TOKEN": "fake-token", "NOTION_DATABASE_ID": "fake-db"}):
        with patch("agent.rag.runbook_agent.similarity_search") as mock_search:
            mock_search.return_value = []
            result = query_runbooks("What is the runbook for database failover?")
            assert isinstance(result, dict)
            assert "answer" in result
            assert "sources" in result
            assert result["ok"] is True
            assert result["sources"] == []


def test_query_runbooks_without_notion_token() -> None:
    with patch.dict(os.environ, {"GCP_PROJECT_ID": "test-project", "NOTION_TOKEN": ""}):
        with patch("agent.rag.runbook_agent.similarity_search") as mock_search:
            mock_search.return_value = []
            result = query_runbooks("Test query")
            # Should not raise an exception, but handle gracefully
            assert isinstance(result, dict)
            assert result["ok"] is True
            assert "answer" in result
            assert "sources" in result

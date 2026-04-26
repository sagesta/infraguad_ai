"""Notion API loader — fetches runbook pages as LangChain Documents."""

from __future__ import annotations

import logging
import os
from typing import Any

from langchain_core.documents import Document

logger = logging.getLogger(__name__)


def _extract_text_from_blocks(blocks: list[dict[str, Any]]) -> str:
    """Recursively extract plain text from Notion block objects."""
    lines: list[str] = []
    for block in blocks:
        block_type = block.get("type", "")
        content = block.get(block_type, {})

        # Extract rich_text content
        rich_texts = content.get("rich_text", [])
        if rich_texts:
            text = "".join(rt.get("plain_text", "") for rt in rich_texts)
            if text.strip():
                lines.append(text.strip())

        # Handle child blocks if present
        children = block.get("children", [])
        if children:
            child_text = _extract_text_from_blocks(children)
            if child_text:
                lines.append(child_text)

    return "\n".join(lines)


def _get_page_title(page: dict[str, Any]) -> str:
    """Extract title from a Notion page object."""
    props = page.get("properties", {})
    for prop in props.values():
        if prop.get("type") == "title":
            title_items = prop.get("title", [])
            return "".join(t.get("plain_text", "") for t in title_items)
    return "Untitled"


def load_notion_runbooks() -> list[Document]:
    """Fetch all pages from a Notion database and return as LangChain Documents.

    Requires env vars:
    - NOTION_TOKEN: Notion integration token
    - NOTION_DATABASE_ID: ID of the database containing runbooks

    Returns:
        List of LangChain Document objects with page content and metadata.
    """
    token = os.environ.get("NOTION_TOKEN", "").strip()
    database_id = os.environ.get("NOTION_DATABASE_ID", "").strip()

    if not token or not database_id:
        logger.warning("NOTION_TOKEN or NOTION_DATABASE_ID not set — skipping runbook load")
        return []

    try:
        from notion_client import Client as NotionClient

        notion = NotionClient(auth=token)

        # Query all pages in the database
        results: list[dict[str, Any]] = []
        has_more = True
        start_cursor: str | None = None

        while has_more:
            kwargs: dict[str, Any] = {"database_id": database_id}
            if start_cursor:
                kwargs["start_cursor"] = start_cursor
            response = notion.databases.query(**kwargs)
            results.extend(response.get("results", []))
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")

        documents: list[Document] = []
        for page in results:
            page_id = page["id"]
            title = _get_page_title(page)

            # Fetch all blocks for this page
            blocks: list[dict[str, Any]] = []
            block_has_more = True
            block_cursor: str | None = None

            while block_has_more:
                bkwargs: dict[str, Any] = {"block_id": page_id}
                if block_cursor:
                    bkwargs["start_cursor"] = block_cursor
                block_resp = notion.blocks.children.list(**bkwargs)
                blocks.extend(block_resp.get("results", []))
                block_has_more = block_resp.get("has_more", False)
                block_cursor = block_resp.get("next_cursor")

            content = _extract_text_from_blocks(blocks)
            if content.strip():
                documents.append(Document(
                    page_content=content,
                    metadata={
                        "source": f"notion://{page_id}",
                        "title": title,
                        "page_id": page_id,
                    },
                ))

        logger.info("Loaded %d runbook documents from Notion", len(documents))
        return documents

    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to load Notion runbooks: %s", exc)
        return []

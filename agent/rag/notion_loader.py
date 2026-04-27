"""Notion API loader — fetches runbook pages as LangChain Documents."""

from __future__ import annotations

import logging
import os
from typing import Any

from langchain_core.documents import Document

logger = logging.getLogger(__name__)


def _extract_text_from_blocks(blocks: list[dict[str, Any]]) -> str:
    """Recursively extract plain text from Notion block objects with basic formatting."""
    lines: list[str] = []
    for block in blocks:
        block_type = block.get("type", "")
        content = block.get(block_type, {})
        rich_texts = content.get("rich_text", [])
        text = "".join(rt.get("plain_text", "") for rt in rich_texts).strip()

        if not text and block_type != "divider":
            # Handle child blocks if present (recursive)
            children = block.get("children", [])
            if children:
                child_text = _extract_text_from_blocks(children)
                if child_text:
                    lines.append(child_text)
            continue

        # INFRAGUARD-NOTION: Preserving headings and lists
        if block_type == "heading_1":
            lines.append(f"# {text}")
        elif block_type == "heading_2":
            lines.append(f"## {text}")
        elif block_type == "heading_3":
            lines.append(f"### {text}")
        elif block_type == "numbered_list_item":
            lines.append(f"1. {text}")
        elif block_type == "bulleted_list_item":
            lines.append(f"- {text}")
        elif text:
            lines.append(text)

    return "\n".join(lines)


def _get_property_value(page: dict[str, Any], prop_name: str) -> str:
    """Extract string value from various Notion property types."""
    props = page.get("properties", {})
    prop = props.get(prop_name, {})
    p_type = prop.get("type")

    if p_type == "select":
        return prop.get("select", {}).get("name") or ""
    if p_type == "status":
        return prop.get("status", {}).get("name") or ""
    if p_type == "multi_select":
        return ", ".join(s.get("name", "") for s in prop.get("multi_select", []))
    if p_type == "title":
        return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    return ""


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
            
            # INFRAGUARD-NOTION: Extract requested metadata
            title = _get_property_value(page, "Name") or "Untitled"
            severity = _get_property_value(page, "Severity")
            environment = _get_property_value(page, "Environment")
            category = _get_property_value(page, "Category")
            status = _get_property_value(page, "Status")

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
                        "severity": severity,
                        "environment": environment,
                        "category": category,
                        "status": status,
                    },
                ))

        logger.info("Loaded %d runbook documents from Notion", len(documents))
        return documents

    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to load Notion runbooks: %s", exc)
        return []

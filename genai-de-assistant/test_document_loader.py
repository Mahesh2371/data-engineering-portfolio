"""
tests/test_document_loader.py
------------------------------
Unit tests for document_loader.py - no API calls needed.
"""

import sys
import os
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from document_loader import load_markdown_files, load_all_documents


def create_temp_md(content: str) -> tuple:
    """Create a temp markdown file and return (dir, filename)."""
    tmpdir = tempfile.mkdtemp()
    filepath = os.path.join(tmpdir, "test_doc.md")
    with open(filepath, "w") as f:
        f.write(content)
    return tmpdir, "test_doc.md"


class TestLoadMarkdownFiles:
    def test_loads_single_file(self):
        content = "# Runbook\n\nThis is a test runbook.\n\n## Section\nDetails here."
        tmpdir, filename = create_temp_md(content)
        docs = load_markdown_files(tmpdir, "runbook")
        assert len(docs) == 1
        assert docs[0].metadata["source"] == filename
        assert docs[0].metadata["type"] == "runbook"
        assert "test runbook" in docs[0].page_content

    def test_empty_directory(self):
        tmpdir = tempfile.mkdtemp()
        docs = load_markdown_files(tmpdir, "runbook")
        assert docs == []

    def test_nonexistent_directory(self):
        docs = load_markdown_files("/nonexistent/path", "runbook")
        assert docs == []

    def test_correct_doc_type_metadata(self):
        content = "# Incident\n\nINC-001 details."
        tmpdir, _ = create_temp_md(content)
        docs = load_markdown_files(tmpdir, "incident_log")
        assert docs[0].metadata["type"] == "incident_log"


class TestLoadAllDocuments:
    def test_returns_list_of_documents(self):
        docs = load_all_documents()
        # Should load the sample runbooks and incident logs in data/
        assert isinstance(docs, list)
        assert len(docs) > 0

    def test_chunks_are_not_too_long(self):
        docs = load_all_documents()
        for doc in docs:
            # Each chunk should be under CHUNK_SIZE + small buffer for overlap
            assert len(doc.page_content) <= 700, f"Chunk too long: {len(doc.page_content)}"

    def test_metadata_preserved_in_chunks(self):
        docs = load_all_documents()
        for doc in docs:
            assert "source" in doc.metadata
            assert "type" in doc.metadata
            assert doc.metadata["type"] in ("runbook", "incident_log")

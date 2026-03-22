"""
document_loader.py
------------------
Loads pipeline runbooks and incident logs from the data directory.
Splits documents into overlapping chunks for FAISS indexing.
"""

import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RUNBOOKS_DIR = os.path.join(DATA_DIR, "runbooks")
INCIDENT_LOGS_DIR = os.path.join(DATA_DIR, "incident_logs")

# Chunk size tuned for DE runbooks: large enough for context, small enough for precision
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def load_markdown_files(directory: str, doc_type: str) -> List[Document]:
    """
    Read all .md files in a directory and return as LangChain Document objects.
    Adds metadata: source filename and document type (runbook / incident_log).
    """
    documents = []
    if not os.path.exists(directory):
        print(f"[WARN] Directory not found: {directory}")
        return documents

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            documents.append(
                Document(
                    page_content=content,
                    metadata={"source": filename, "type": doc_type},
                )
            )
            print(f"[INFO] Loaded {doc_type}: {filename}")

    return documents


def load_all_documents() -> List[Document]:
    """Load runbooks + incident logs and split into chunks."""
    raw_docs: List[Document] = []
    raw_docs.extend(load_markdown_files(RUNBOOKS_DIR, "runbook"))
    raw_docs.extend(load_markdown_files(INCIDENT_LOGS_DIR, "incident_log"))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"[INFO] Total chunks created: {len(chunks)}")
    return chunks


if __name__ == "__main__":
    docs = load_all_documents()
    for i, doc in enumerate(docs[:3]):
        print(f"\n--- Chunk {i+1} [{doc.metadata}] ---")
        print(doc.page_content[:200])

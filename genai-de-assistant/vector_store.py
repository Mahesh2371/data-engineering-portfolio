"""
vector_store.py
---------------
Builds a FAISS vector store from document chunks using OpenAI embeddings.
Persists the index to disk so Lambda cold starts are fast.
"""

import os
import pickle
from typing import List

from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "faiss_index")


def get_embeddings() -> OpenAIEmbeddings:
    """Return OpenAI embeddings. API key read from environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable not set. "
            "Set it before building the vector store."
        )
    return OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-3-small")


def build_vector_store(documents: List[Document]) -> FAISS:
    """
    Build FAISS index from document chunks and save to disk.
    Run this once locally (or in a build step) before deploying to Lambda.
    """
    print(f"[INFO] Building FAISS index from {len(documents)} chunks...")
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"[INFO] FAISS index saved to: {FAISS_INDEX_PATH}")
    return vector_store


def load_vector_store() -> FAISS:
    """
    Load pre-built FAISS index from disk.
    Called at Lambda cold start or local runtime.
    """
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(
            f"FAISS index not found at {FAISS_INDEX_PATH}. "
            "Run build_index.py first to generate the index."
        )
    embeddings = get_embeddings()
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    print("[INFO] FAISS index loaded successfully.")
    return vector_store


def similarity_search(query: str, k: int = 4) -> List[Document]:
    """Retrieve top-k most relevant document chunks for a query."""
    vector_store = load_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results


if __name__ == "__main__":
    # Quick test: load index and run a sample query
    results = similarity_search("What causes Spark OOM errors?")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} [{doc.metadata}] ---")
        print(doc.page_content[:300])

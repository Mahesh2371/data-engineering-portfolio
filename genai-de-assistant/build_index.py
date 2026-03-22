"""
build_index.py
--------------
One-time script to build the FAISS vector index from runbooks + incident logs.
Run this locally before deploying to Lambda, or as a CI/CD build step.

Usage:
    export OPENAI_API_KEY=sk-...
    python build_index.py
"""

import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from document_loader import load_all_documents
from vector_store import build_vector_store


def main():
    print("=" * 50)
    print("GenAI DE Assistant - FAISS Index Builder")
    print("=" * 50)

    if not os.environ.get("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY not set. Exiting.")
        sys.exit(1)

    # Load and chunk all documents
    documents = load_all_documents()
    if not documents:
        print("[ERROR] No documents loaded. Check data/ directory.")
        sys.exit(1)

    # Build and save FAISS index
    build_vector_store(documents)
    print("\n✅ FAISS index built successfully!")
    print("You can now run the assistant locally or deploy to Lambda.")


if __name__ == "__main__":
    main()

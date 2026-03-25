import os
import sqlite3
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from transformers import pipeline


DOCS_DIR = Path("docs")
DB_PATH = "embeddings.db"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))
        start += size - overlap
    return chunks


class RAGPipeline:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_new_tokens=200,
        )
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()
        self._doc_names: list[str] = []

    def _init_db(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                content TEXT,
                embedding BLOB
            )
            """
        )
        self.conn.commit()

    def _clear_db(self):
        self.conn.execute("DELETE FROM chunks")
        self.conn.commit()

    def build_index(self):
        self._clear_db()
        self._doc_names = []

        for filepath in DOCS_DIR.glob("*.md"):
            self._doc_names.append(filepath.name)
            text = filepath.read_text(encoding="utf-8")
            chunks = chunk_text(text)

            for chunk in chunks:
                embedding = self.embedder.encode(chunk, convert_to_numpy=True)
                self.conn.execute(
                    "INSERT INTO chunks (source, content, embedding) VALUES (?, ?, ?)",
                    (filepath.name, chunk, embedding.tobytes()),
                )

        self.conn.commit()

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    def retrieve(self, query: str, top_k: int = TOP_K) -> list[dict]:
        query_vec = self.embedder.encode(query, convert_to_numpy=True)

        rows = self.conn.execute("SELECT source, content, embedding FROM chunks").fetchall()

        scored = []
        for source, content, emb_bytes in rows:
            stored_vec = np.frombuffer(emb_bytes, dtype=np.float32)
            score = self._cosine_similarity(query_vec, stored_vec)
            scored.append({"source": source, "content": content, "score": score})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def query(self, user_query: str) -> tuple[str, str]:
        retrieved = self.retrieve(user_query)

        if not retrieved:
            return "I couldn't find relevant information in the knowledge base.", "None"

        context = "\n\n".join(r["content"] for r in retrieved)
        sources = ", ".join(sorted(set(r["source"] for r in retrieved)))

        prompt = (
            f"Answer the question based only on the context below.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {user_query}\n\n"
            f"Answer:"
        )

        result = self.generator(prompt, max_new_tokens=200, truncation=True)
        answer = result[0]["generated_text"].strip()

        if not answer:
            answer = "I found related content but couldn't generate a clear answer. Please refine your question."

        return answer, sources

    def list_documents(self) -> list[str]:
        return self._doc_names if self._doc_names else ["No documents indexed yet."]

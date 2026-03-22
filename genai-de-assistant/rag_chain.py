"""
rag_chain.py
------------
Core RAG pipeline.
Retrieves relevant context from FAISS, then calls GPT-4 to generate answers
grounded in pipeline runbooks and incident logs.
"""

import os
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from vector_store import load_vector_store


# ── Prompt Template ─────────────────────────────────────────────────────────
# Keeps the LLM focused on DE runbooks/incidents; avoids hallucination.

SYSTEM_PROMPT_TEMPLATE = """You are a Data Engineering Assistant specializing in
pipeline runbooks and incident logs for a Banking & Financial Services data platform.

Use ONLY the context below to answer the question. If the answer is not in the
context, say "I don't have information on that in the runbooks or incident logs."
Do NOT make up answers.

Context:
{context}

Question: {question}

Answer (be concise, specific, and use bullet points where helpful):"""

PROMPT = PromptTemplate(
    template=SYSTEM_PROMPT_TEMPLATE,
    input_variables=["context", "question"],
)


def build_rag_chain() -> RetrievalQA:
    """
    Build the LangChain RetrievalQA chain.
    - Retriever: FAISS vector store (top 4 chunks)
    - LLM: GPT-4 (temperature=0 for deterministic answers)
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name="gpt-4",
        temperature=0,  # Deterministic for ops use cases
        max_tokens=512,
    )

    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,  # Include sources in response for transparency
    )
    return chain


def query_assistant(question: str) -> Dict[str, Any]:
    """
    Main entry point: query the RAG assistant with a natural language question.

    Returns:
        dict with keys:
          - answer (str): GPT-4 response grounded in runbooks/incidents
          - sources (list): list of source document names used
    """
    chain = build_rag_chain()
    result = chain.invoke({"query": question})

    answer = result.get("result", "").strip()
    source_docs = result.get("source_documents", [])
    sources = list({doc.metadata.get("source", "unknown") for doc in source_docs})

    return {
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    # Local smoke test
    test_questions = [
        "How do I fix an S3 permission error in the ETL pipeline?",
        "What should I do if Kafka consumer lag spikes?",
        "What caused the schema mismatch incident in April 2024?",
    ]
    for q in test_questions:
        print(f"\nQ: {q}")
        response = query_assistant(q)
        print(f"A: {response['answer']}")
        print(f"Sources: {response['sources']}")

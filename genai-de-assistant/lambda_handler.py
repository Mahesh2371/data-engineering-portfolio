"""
lambda_handler.py
-----------------
AWS Lambda entry point for the GenAI Data Engineering Assistant.

Flow:
  Slack slash command → API Gateway → Lambda → RAG chain (FAISS + GPT-4) → Slack response

Slack requires a response within 3 seconds. For longer RAG queries,
this handler returns HTTP 200 immediately with a "processing" message,
then posts the actual answer asynchronously via Slack response_url.
"""

import json
import os
import urllib.parse
import urllib.request
from typing import Any, Dict

# Local imports (packaged into Lambda deployment zip)
from src.rag_chain import query_assistant
from src.slack_handler import (
    format_slack_response,
    parse_slack_payload,
    verify_slack_signature,
)


def post_to_slack(response_url: str, payload: Dict[str, Any]) -> None:
    """Post the final RAG response back to Slack via response_url (async)."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        response_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        pass  # Fire and forget


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler.

    Triggered by: API Gateway POST /de-assistant
    Expected input: Slack slash command URL-encoded body

    Returns: Immediate HTTP 200 to satisfy Slack's 3-second timeout,
             then posts answer to Slack response_url.
    """
    # ── 1. Parse incoming request ──────────────────────────────────────────
    body = event.get("body", "")
    headers = event.get("headers", {})

    # ── 2. Verify Slack signature (security) ──────────────────────────────
    timestamp = headers.get("X-Slack-Request-Timestamp", "")
    signature = headers.get("X-Slack-Signature", "")

    if not verify_slack_signature(body, timestamp, signature):
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Invalid Slack signature"}),
        }

    # ── 3. Parse Slack payload ─────────────────────────────────────────────
    params = parse_slack_payload(body)
    question = params.get("text", "").strip()
    user = params.get("user_name", "unknown")
    response_url = params.get("response_url", "")

    if not question:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "response_type": "ephemeral",
                "text": "⚠️ Please provide a question. Usage: `/de-assist <your question>`",
            }),
        }

    print(f"[INFO] User: {user} | Question: {question}")

    # ── 4. Acknowledge immediately (Slack 3-second rule) ──────────────────
    ack_response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "response_type": "ephemeral",
            "text": f"🔍 Searching runbooks and incident logs for: _{question}_",
        }),
    }

    # ── 5. Run RAG query ───────────────────────────────────────────────────
    try:
        result = query_assistant(question)
        slack_payload = format_slack_response(
            answer=result["answer"],
            sources=result["sources"],
            question=question,
        )
        print(f"[INFO] Answer generated. Sources: {result['sources']}")

    except Exception as e:
        print(f"[ERROR] RAG query failed: {e}")
        slack_payload = {
            "response_type": "ephemeral",
            "text": f"❌ Error processing your question. Please check the logs. (`{str(e)}`)",
        }

    # ── 6. Post final answer to Slack ──────────────────────────────────────
    if response_url:
        try:
            post_to_slack(response_url, slack_payload)
        except Exception as e:
            print(f"[ERROR] Failed to post to Slack: {e}")

    return ack_response

"""
slack_handler.py
----------------
Handles Slack slash command payloads.
Parses the incoming request from Slack, calls the RAG chain,
and formats the response as a Slack Block Kit message.
"""

import hashlib
import hmac
import os
import time
from typing import Dict, Any


def verify_slack_signature(body: str, timestamp: str, signature: str) -> bool:
    """
    Verify Slack request signature to ensure requests are from Slack.
    https://api.slack.com/authentication/verifying-requests-from-slack
    """
    slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
    base_string = f"v0:{timestamp}:{body}"
    computed = "v0=" + hmac.new(
        slack_signing_secret.encode(),
        base_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    # Also check timestamp to prevent replay attacks (within 5 minutes)
    if abs(time.time() - int(timestamp)) > 300:
        return False

    return hmac.compare_digest(computed, signature)


def parse_slack_payload(body: str) -> Dict[str, str]:
    """
    Parse URL-encoded Slack slash command body.
    Returns dict with keys: text, user_name, channel_name, command.
    """
    params = {}
    for pair in body.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            params[key] = value.replace("+", " ").replace("%20", " ")
    return params


def format_slack_response(answer: str, sources: list, question: str) -> Dict[str, Any]:
    """
    Format RAG response as Slack Block Kit message.
    Includes the question, answer, and source documents cited.
    """
    source_text = " | ".join(sources) if sources else "No sources found"

    return {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🤖 DE Assistant Response",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Question:* {question}",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Answer:*\n{answer}",
                },
            },
            {"type": "divider"},
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"📄 *Sources:* {source_text}",
                    }
                ],
            },
        ],
    }

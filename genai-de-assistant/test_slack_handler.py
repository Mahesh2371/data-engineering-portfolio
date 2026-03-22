"""
tests/test_slack_handler.py
----------------------------
Unit tests for slack_handler.py - no API calls needed.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from slack_handler import parse_slack_payload, format_slack_response


class TestParseSlackPayload:
    def test_parses_basic_payload(self):
        body = "text=how+do+I+fix+OOM&user_name=mahesh&channel_name=de-oncall&command=%2Fde-assist"
        result = parse_slack_payload(body)
        assert result["text"] == "how do I fix OOM"
        assert result["user_name"] == "mahesh"
        assert result["channel_name"] == "de-oncall"

    def test_empty_body(self):
        result = parse_slack_payload("")
        assert result == {}

    def test_missing_text_key(self):
        body = "user_name=mahesh&channel_name=de-oncall"
        result = parse_slack_payload(body)
        assert "text" not in result
        assert result["user_name"] == "mahesh"


class TestFormatSlackResponse:
    def test_response_has_blocks(self):
        response = format_slack_response(
            answer="Increase executor memory to 8g.",
            sources=["etl_pipeline_runbook.md"],
            question="How to fix Spark OOM?",
        )
        assert "blocks" in response
        assert response["response_type"] == "in_channel"

    def test_response_contains_answer(self):
        answer = "Check IAM role permissions."
        response = format_slack_response(answer, ["runbook.md"], "S3 permission error?")
        # Flatten all block text
        all_text = str(response)
        assert answer in all_text

    def test_response_contains_source(self):
        response = format_slack_response("Answer here.", ["etl_pipeline_runbook.md"], "Q?")
        all_text = str(response)
        assert "etl_pipeline_runbook.md" in all_text

    def test_no_sources_handled_gracefully(self):
        response = format_slack_response("Answer.", [], "Question?")
        all_text = str(response)
        assert "No sources found" in all_text

    def test_multiple_sources(self):
        sources = ["runbook1.md", "incident_log.md"]
        response = format_slack_response("Answer.", sources, "Question?")
        all_text = str(response)
        assert "runbook1.md" in all_text
        assert "incident_log.md" in all_text

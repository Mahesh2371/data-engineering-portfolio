"""
local_chat.py
-------------
Interactive CLI to test the GenAI DE Assistant locally
without needing Slack or AWS Lambda.

Usage:
    export OPENAI_API_KEY=sk-...
    python local_chat.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from rag_chain import query_assistant

WELCOME = """
╔══════════════════════════════════════════════════════╗
║       🤖 GenAI Data Engineering Assistant            ║
║  Ask questions about pipelines, runbooks & incidents ║
║  Type 'exit' or 'quit' to stop                       ║
╚══════════════════════════════════════════════════════╝

Sample questions:
  - How do I fix an S3 permission error?
  - What caused the Kafka lag spike incident?
  - How do I restart the streaming pipeline?
  - What is the Silver layer transformation process?
"""


def main():
    print(WELCOME)

    if not os.environ.get("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY environment variable not set.")
        print("Export it first: export OPENAI_API_KEY=sk-...")
        sys.exit(1)

    while True:
        try:
            question = input("\n💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        print("\n🔍 Searching runbooks and incident logs...")
        try:
            result = query_assistant(question)
            print(f"\n🤖 Assistant:\n{result['answer']}")
            if result["sources"]:
                print(f"\n📄 Sources: {', '.join(result['sources'])}")
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

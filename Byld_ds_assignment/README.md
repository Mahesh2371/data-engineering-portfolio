# Discord RAG Bot

A Discord bot that answers questions from a local knowledge base using Retrieval-Augmented Generation (RAG). Built with `discord.py`, `sentence-transformers` for semantic embeddings, `SQLite` for vector storage, and `google/flan-t5-base` from Hugging Face for answer generation — no paid APIs required.

---

## How It Works

```
User Query
    │
    ▼
Embed query  ──►  all-MiniLM-L6-v2
    │
    ▼
Cosine similarity search  ──►  SQLite (chunk embeddings)
    │
    ▼
Top-K chunks retrieved
    │
    ▼
Prompt built  ──►  "Answer based on context: ..."
    │
    ▼
flan-t5-base generates answer
    │
    ▼
Discord embed reply with source attribution
```

**Models used:**
| Role | Model | Why |
|------|-------|-----|
| Embeddings | `all-MiniLM-L6-v2` | Lightweight, fast, good semantic quality |
| Answer generation | `google/flan-t5-base` | Instruction-following T5 model, runs on CPU |
| Vector storage | SQLite (native) | Zero-dependency local store, no server needed |

---

## Project Structure

```
discord-rag-bot/
├── bot.py                  # Discord bot entry point
├── src/
│   └── rag.py              # Chunking, embedding, retrieval, generation
├── docs/                   # Knowledge base (Markdown files)
│   ├── python_faq.md
│   ├── ml_concepts.md
│   ├── data_engineering.md
│   └── sql_reference.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore
```

---

## Setup & Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/discord-rag-bot.git
cd discord-rag-bot
```

### 2. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application → Bot → copy the token
3. Enable **Message Content Intent** under Bot settings
4. Invite the bot to your server with the `bot` + `applications.commands` scope

### 3. Configure environment

```bash
cp .env.example .env
# Paste your Discord token into .env
```

### 4. Install dependencies

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run

```bash
python bot.py
```

On first run, models are downloaded from Hugging Face (~90 MB total) and documents are indexed into `embeddings.db`.

---

## Running with Docker

```bash
docker compose up --build
```

---

## Bot Commands

| Command | Description |
|---------|-------------|
| `/ask <question>` | Ask anything from the knowledge base |
| `/sources` | List indexed documents |
| `/help` | Show all available commands |

**Example:**
```
/ask What is the Medallion Architecture?
/ask How does gradient descent work?
/ask What is the difference between RANK and DENSE_RANK?
```

---

## Adding Your Own Documents

Drop any `.md` file into the `docs/` folder and restart the bot. The index rebuilds automatically on startup.

---

## Design Decisions

- **SQLite over a vector DB**: Keeps the stack minimal with zero infrastructure. For larger corpora, swapping to `chromadb` or `qdrant` is straightforward.
- **flan-t5-base over LLaMA**: Runs on CPU without GPU, making it portable and easy to evaluate. The instruction-tuned format fits the RAG prompt pattern well.
- **Chunking with overlap**: A 50-word overlap between chunks prevents context loss at boundaries, improving retrieval quality on longer passages.
- **Source attribution**: Every response includes the source document names so evaluators and users can verify answers.

---

## Requirements

- Python 3.10+
- ~500 MB disk space (model cache)
- No GPU required

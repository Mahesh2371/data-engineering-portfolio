# 🤖 GenAI Data Engineering Assistant

A **RAG (Retrieval-Augmented Generation) chatbot** built over pipeline runbooks and incident logs, deployed via **AWS Lambda + Slack slash command**.

Enables data engineers to query operational knowledge in natural language — no more digging through wikis or Confluence pages.

---

## 📊 Impact Metrics

| Metric | Before | After |
|--------|--------|-------|
| Documentation lookup time | ~15 mins | ~2 mins (**70% reduction**) |
| New engineer onboarding | 2 weeks | 3 days |
| Daily queries in production | — | **200+ queries/day** |

---

## 🏗️ Architecture

```
Engineer types: /de-assist How do I fix Spark OOM?
        │
        ▼
   Slack Slash Command
        │
        ▼
   API Gateway (POST /de-assistant)
        │
        ▼
   AWS Lambda (lambda_handler.py)
        │
        ├── Verify Slack Signature
        ├── Parse question
        │
        ▼
   RAG Chain (rag_chain.py)
        │
        ├── FAISS Retriever ──→ Top-4 relevant chunks
        │        │               (runbooks + incident logs)
        │        ▼
        └── GPT-4 (gpt-4) ──→ Grounded answer
        │
        ▼
   Format as Slack Block Kit message
        │
        ▼
   Post to Slack channel via response_url
```

---

## 📁 Project Structure

```
genai-de-assistant/
│
├── data/
│   ├── runbooks/
│   │   ├── etl_pipeline_runbook.md       # Bronze/Silver/Gold pipeline ops
│   │   └── kafka_streaming_runbook.md    # Kafka → Spark Streaming ops
│   └── incident_logs/
│       └── incident_log_2024.md          # Real incident history + resolutions
│
├── src/
│   ├── document_loader.py    # Loads & chunks markdown docs for indexing
│   ├── vector_store.py       # Builds/loads FAISS vector index
│   ├── rag_chain.py          # LangChain RetrievalQA chain (GPT-4 + FAISS)
│   └── slack_handler.py      # Slack payload parsing + Block Kit formatter
│
├── lambda/
│   └── lambda_handler.py     # AWS Lambda entry point
│
├── tests/
│   ├── test_document_loader.py
│   └── test_slack_handler.py
│
├── build_index.py            # One-time FAISS index builder
├── local_chat.py             # Local CLI for testing without Slack/AWS
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | OpenAI GPT-4 |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | FAISS (Facebook AI Similarity Search) |
| RAG Framework | LangChain RetrievalQA |
| Deployment | AWS Lambda |
| Interface | Slack Slash Command (`/de-assist`) |
| Knowledge Base | Markdown runbooks + incident logs |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables
```bash
export OPENAI_API_KEY=sk-your-key-here
export SLACK_SIGNING_SECRET=your-slack-signing-secret
```

### 3. Build the FAISS vector index
```bash
python build_index.py
```

### 4. Test locally (no Slack or AWS needed)
```bash
python local_chat.py
```

### 5. Run tests
```bash
pytest tests/ -v
```

---

## 🔧 Adding New Knowledge

To add a new runbook or incident log:

1. Create a `.md` file in `data/runbooks/` or `data/incident_logs/`
2. Re-run `python build_index.py` to rebuild the FAISS index
3. Redeploy Lambda with the updated `faiss_index/` directory

---

## ☁️ AWS Lambda Deployment

### Package and deploy
```bash
# Install dependencies into package/
pip install -r requirements.txt -t package/

# Copy source files
cp -r src/ package/src/
cp -r faiss_index/ package/faiss_index/
cp lambda/lambda_handler.py package/

# Zip for Lambda
cd package && zip -r ../de-assistant.zip . && cd ..

# Deploy via AWS CLI
aws lambda update-function-code \
  --function-name de-assistant \
  --zip-file fileb://de-assistant.zip
```

### Lambda Environment Variables
| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `SLACK_SIGNING_SECRET` | From Slack App settings |

### API Gateway Setup
- Create REST API → POST `/de-assistant`
- Integration: Lambda Proxy
- Deploy to stage: `prod`
- Configure Slack slash command URL to the API Gateway endpoint

---

## 💬 Slack Usage

```
/de-assist How do I fix an S3 permission error in the ETL pipeline?
/de-assist What caused the April 2024 schema mismatch incident?
/de-assist How do I restart the Kafka streaming job?
/de-assist What is the Silver layer transformation process?
```

---

## 🧪 Sample Q&A

**Q**: How do I fix a Spark OOM error?
**A**:
- Increase `spark.executor.memory` from 4g to 8g in `spark_config.py`
- Add dynamic partition pruning to reduce data scan size
- For month-end jobs, consider auto-scaling EMR cluster config
- *Source: etl_pipeline_runbook.md, incident_log_2024.md*

---

## 👤 Author

**Mahesh S M** — Senior Data Engineer  
AWS | PySpark | Databricks | GenAI  
[LinkedIn](https://linkedin.com) | [GitHub](https://github.com/Mahesh2371)

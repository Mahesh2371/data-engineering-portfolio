# 🚀 Data Engineering Poftfolio
![Profile Views](https://komarev.com/ghpvc/?username=Mahesh2371&color=blue)

End-to-end Data Engineering platform demonstrating both **Real-Time Streaming** and **Batch Lakehouse ETL** architectures using modern Big Data tools.

This repository showcases production-style implementations using:

✅ PySpark  
✅ Kafka
✅ SQL
✅ Delta Lake  
✅ AWS S3 (local simulation)  
✅ Apache Airflow  
✅ Docker  

---

## 📌 Projects Included

### 1️⃣ Streaming Pipeline
Kafka → Spark Structured Streaming → Delta Lake

• Real-time ingestion of transactions  
• Aggregations & transformations  
• Low-latency processing  
• Fault-tolerant checkpoints  
Folder: `/streaming-pipeline`

---

### 2️⃣ Batch Lakehouse ETL
S3 → Spark → Delta → Analytics tables

• Batch ingestion  
• Data cleansing & transformations  
• Star schema modeling  
• Airflow orchestration  
Folder: `/batch-lakehouse-etl`

---

## 🏗️ Architecture

### Streaming
Producer → Kafka → Spark → Delta Lake → Analytics

### Batch
Raw → Spark ETL → Delta Lake → Data Marts → BI

---

## ⚙️ Tech Stack

| Category | Tools |
|----------|---------------------------|
| Processing | PySpark, Spark SQL |
| Streaming | Kafka |
| Storage | Delta Lake, S3 |
| Orchestration | Airflow |
| DevOps | Docker |
| Language | Python |

---

## 🚀 Quick Start (Docker)

### Step 1
```
docker-compose up --build
```

### Step 2
Run streaming producer
```
python streaming-pipeline/producer/transaction_producer.py
```

### Step 3
Run Spark job
```
spark-submit streaming-pipeline/spark/stream_processor.py
```

### Step 4
Access Airflow
```
http://localhost:8080
```

---

## 📊 Outcomes

✔ Real-time processing  
✔ Batch ETL  
✔ Lakehouse architecture  
✔ Production-ready design  
✔ Resume-ready project

---

## 👤 Author
Mahesh S M  
Senior Data Engineer  

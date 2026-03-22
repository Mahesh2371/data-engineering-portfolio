# Kafka → Spark Streaming Pipeline Runbook

## Overview
Real-time transaction stream ingested from Kafka topic `transactions-raw`,
processed via Spark Structured Streaming, and written to Delta Lake.

## Kafka Configuration
- Broker: `kafka:9092`
- Topic: `transactions-raw`
- Consumer Group: `spark-streaming-group`
- Starting Offsets: `latest` (production), `earliest` (backfill)
- Checkpoint Location: `s3://citi-checkpoints/streaming/transactions/`

## Spark Streaming Job
- Entry Point: `streaming-pipeline/spark/stream_processor.py`
- Trigger: `processingTime='30 seconds'`
- Output Mode: `append`
- Watermark: 10 minutes on `event_time` to handle late arrivals
- Parallelism: `spark.sql.shuffle.partitions=200`

## Starting the Pipeline
```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.streaming.kafka.maxRatePerPartition=1000 \
  streaming-pipeline/spark/stream_processor.py
```

## Monitoring
- Spark UI: `http://<driver-host>:4040`
- Kafka Lag: Monitor via `kafka-consumer-groups.sh --describe --group spark-streaming-group`
- Delta Table: Query `streaming_transactions` in Databricks SQL

## Common Issues & Resolutions
- **Consumer Lag Spike**: Scale up Spark executors or increase Kafka partitions
- **Checkpoint Corruption**: Delete checkpoint dir and restart with `earliest` offset
- **Deserialization Error**: Check if Kafka message schema changed; update `schema.py`
- **Job Stuck**: Check for shuffle spill; increase `spark.executor.memory` to 8g
- **Delta Write Conflicts**: Enable `optimisticTransaction` and retry logic in writer

## Restart Procedure
1. Kill existing Spark job via YARN RM or `yarn application -kill <app_id>`
2. Verify Kafka lag returns to 0
3. Resubmit with `spark-submit`
4. Monitor Spark UI for 5 minutes

## SLA
- Maximum acceptable lag: 5 minutes
- Alert threshold: >10k messages in backlog
- Slack alert channel: #streaming-alerts

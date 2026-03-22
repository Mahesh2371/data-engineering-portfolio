# ETL Pipeline Runbook

## Overview
The ETL pipeline ingests raw transaction data from S3, transforms it using PySpark,
and loads it into Delta Lake tables following the Medallion Architecture (Bronze → Silver → Gold).

## Pipeline Schedule
- **Batch Jobs**: Triggered daily at 02:00 UTC via Apache Airflow DAG `etl_daily_batch`
- **Streaming Jobs**: 24/7 real-time via Spark Structured Streaming

## Bronze Layer - Raw Ingestion
- Source: S3 bucket `s3://citi-raw-data/transactions/`
- Format: Parquet, JSON, CSV
- No transformations applied; raw data preserved
- Partition by: `year/month/day`
- Airflow Task: `ingest_raw_to_bronze`

## Silver Layer - Cleansed Data
- Reads from Bronze Delta table
- Applies schema validation and data type casting
- Removes duplicates using `transaction_id` as primary key
- Handles nulls: fills missing `amount` with 0, drops rows where `customer_id` is null
- LLM anomaly detection layer scans for unusual transaction patterns
- Airflow Task: `transform_bronze_to_silver`

## Gold Layer - Analytics-Ready
- Aggregated fact and dimension tables (Star Schema)
- KPIs: daily transaction volume, customer spend trends, fraud indicators
- Airflow Task: `aggregate_silver_to_gold`

## Common Failure Points
- **S3 Permission Errors**: Check IAM role `etl-pipeline-role` has `s3:GetObject` and `s3:ListBucket`
- **Schema Mismatch**: Source schema may change; validate with `schema_validator.py` before running
- **Spark OOM**: Increase executor memory in `spark_config.py` or reduce partition size
- **Delta Merge Conflicts**: Ensure no concurrent writes; check Airflow task dependency

## Contacts
- Pipeline Owner: Data Engineering Team
- On-call Slack: #de-oncall
- Runbook Version: 2.1

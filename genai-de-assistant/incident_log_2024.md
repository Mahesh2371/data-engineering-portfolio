# Incident Log - Data Engineering Team

---

## INC-2024-001 | 2024-01-15 | SEVERITY: HIGH
**Title**: ETL Bronze ingestion failure - S3 permission denied
**Reporter**: Airflow Alert
**Affected Pipeline**: `etl_daily_batch` - Task `ingest_raw_to_bronze`
**Duration**: 3 hours (02:00 - 05:00 UTC)

**Root Cause**:
IAM role `etl-pipeline-role` policy was accidentally revoked during a routine IAM audit.
The role lost `s3:GetObject` permission on bucket `s3://citi-raw-data/`.

**Resolution**:
Re-attached `S3ReadPolicy` to `etl-pipeline-role`. Ran manual backfill for missed partition `2024-01-15`.

**Prevention**:
Added IAM role validation step in Airflow DAG before S3 read tasks.

---

## INC-2024-002 | 2024-02-03 | SEVERITY: MEDIUM
**Title**: Spark OOM error in Silver transformation
**Reporter**: CloudWatch Alert
**Affected Pipeline**: `etl_daily_batch` - Task `transform_bronze_to_silver`
**Duration**: 1.5 hours

**Root Cause**:
Month-end data volume (5x normal). Executor memory set to 4g was insufficient.
Shuffle spill to disk caused slowdown, then OOM.

**Resolution**:
Increased `spark.executor.memory` from 4g to 8g in `spark_config.py`.
Added dynamic partition pruning to reduce data scan size.

**Prevention**:
Added memory auto-scaling rule in EMR cluster config for end-of-month jobs.

---

## INC-2024-003 | 2024-03-22 | SEVERITY: LOW
**Title**: Kafka consumer lag spike - streaming pipeline delayed
**Reporter**: Grafana Dashboard
**Affected Pipeline**: Kafka → Spark Streaming
**Duration**: 45 minutes

**Root Cause**:
Upstream system pushed 10x normal message volume (load test in prod by mistake).
Spark streaming could not keep up; lag reached 150k messages.

**Resolution**:
Temporarily increased Spark executors from 4 to 10 via YARN.
Lag cleared within 30 minutes.

**Prevention**:
Upstream teams now required to notify #de-oncall before load tests.
Auto-scaling policy added to EMR cluster for streaming jobs.

---

## INC-2024-004 | 2024-04-10 | SEVERITY: HIGH
**Title**: Delta Lake schema mismatch - pipeline aborted
**Reporter**: Airflow Alert
**Affected Pipeline**: `etl_daily_batch` - Silver layer write
**Duration**: 2 hours

**Root Cause**:
Source team added new column `transaction_channel` to upstream table without notifying DE team.
Delta Lake schema enforcement rejected the write.

**Resolution**:
Updated Silver table schema via `ALTER TABLE` in Delta.
Added `mergeSchema=True` option for non-breaking changes.

**Prevention**:
Implemented schema drift detection in `schema_validator.py`.
Source teams must raise a Jira ticket before schema changes.

---

## INC-2024-005 | 2024-06-18 | SEVERITY: MEDIUM
**Title**: Airflow DAG not triggered - missed daily batch
**Reporter**: Data Quality Check Alert
**Affected Pipeline**: `etl_daily_batch`
**Duration**: 6 hours (entire batch window missed)

**Root Cause**:
Airflow scheduler process crashed due to metadata DB connection pool exhaustion.

**Resolution**:
Restarted Airflow scheduler. Increased `sql_alchemy_pool_size` from 5 to 20.
Ran manual DAG trigger for missed date.

**Prevention**:
Added Airflow scheduler health check in CloudWatch.
Alert configured for scheduler process downtime > 5 minutes.

# Data Engineering Concepts

## What is a data pipeline?
A data pipeline is a series of data processing steps where data is ingested from sources, transformed, and loaded into a destination such as a data warehouse or data lake. Pipelines automate and orchestrate these workflows.

## What is ETL?
ETL stands for Extract, Transform, Load. It is a process where data is extracted from source systems, transformed to meet business or analytical requirements, and loaded into a target system.

## What is the difference between ETL and ELT?
In ETL, data is transformed before loading into the target. In ELT, raw data is first loaded into the target system and then transformed in place. ELT is preferred in modern cloud data warehouses due to their processing power.

## What is Apache Spark?
Apache Spark is an open-source distributed computing framework designed for large-scale data processing. It provides APIs in Python, Scala, Java, and R, and supports batch processing, streaming, machine learning, and graph processing.

## What is Delta Lake?
Delta Lake is an open-source storage layer that adds ACID transactions, schema enforcement, and time travel capabilities to data lakes. It sits on top of cloud storage and is tightly integrated with Apache Spark and Databricks.

## What is the Medallion Architecture?
The Medallion Architecture is a data design pattern used in data lakehouses. It organizes data into three layers: Bronze (raw ingested data), Silver (cleaned and enriched data), and Gold (business-level aggregated data ready for reporting).

## What is Apache Airflow?
Apache Airflow is an open-source workflow orchestration tool that allows you to programmatically author, schedule, and monitor data pipelines. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python.

## What is a data warehouse?
A data warehouse is a centralized repository that stores structured, filtered data optimized for analysis and reporting. It typically holds historical data from multiple sources and is organized using dimensional modeling.

## What is partitioning in Spark?
Partitioning divides a large dataset into smaller, manageable chunks distributed across nodes in a cluster. Proper partitioning improves parallelism and query performance. Poor partitioning leads to data skew and slow jobs.

## What is schema-on-read vs schema-on-write?
Schema-on-write enforces a defined schema when data is written (e.g., relational databases). Schema-on-read applies a schema when data is queried, providing flexibility for raw storage (e.g., data lakes with Parquet or JSON files).

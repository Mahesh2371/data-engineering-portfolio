from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("batch_etl", start_date=datetime(2024,1,1), schedule="@daily") as dag:

    ingest = BashOperator(task_id="ingest", bash_command="python ingest.py")
    transform = BashOperator(task_id="transform", bash_command="python transform.py")

    ingest >> transform

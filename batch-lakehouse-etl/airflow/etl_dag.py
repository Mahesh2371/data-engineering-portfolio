from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="batch_etl",
    start_date=datetime(2024,1,1),
    schedule="@daily",
    catchup=False,
    ) as dag:

    ingest = BashOperator(task_id="ingest", bash_command="python /opt/airflow/scripts/ingestion/ingest.py")
    transform = BashOperator(task_id="transform", bash_command="python /opt/airflow/scripts/transform/transform.py")

    ingest >> transform

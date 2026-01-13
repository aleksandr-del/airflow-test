from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from function import print_context

default_args: dict = {
    "owner": "avdel",
    "retries": 1,
    "retry_delay": timedelta(seconds=3),
}

with DAG(
    dag_id="print_context",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 0 * * 1-5",
    tags=["print", "context"],
) as dag:
    start, end = [EmptyOperator(task_id=task) for task in "start end".split()]

    print_context = PythonOperator(
        task_id="print_context", python_callable=print_context
    )

    start >> print_context >> end

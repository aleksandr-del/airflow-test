from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from function import get_even_or_odd_day

default_args = {"owner": "avdel", "retries": 1, "retry_delay": timedelta(seconds=3)}

with DAG(
    dag_id="branch",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 0 * * *",
    tags=["branches"],
) as dag:
    even, odd = (EmptyOperator(task_id=task) for task in "even odd".split())
    branch_option = BranchPythonOperator(
        task_id="branch_option", python_callable=get_even_or_odd_day
    )

    branch_option >> [even, odd]

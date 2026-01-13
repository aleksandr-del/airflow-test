from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import ShortCircuitOperator
from function import get_even

default_args = {"owner": "avdel", "retries": 1, "retry_delay": timedelta(seconds=3)}

with DAG(
    dag_id="circuit",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 0 * * *",
    tags=["circuit"],
) as dag:
    start, task_1, task_2, end = (
        EmptyOperator(task_id=task) for task in "start task_1 task_2 end".split()
    )
    circuit = ShortCircuitOperator(task_id="circuit", python_callable=get_even)

    start >> circuit >> [task_1, task_2] >> end

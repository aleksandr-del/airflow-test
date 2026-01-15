from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from function import on_failure_callback, when_even_raise_exception

default_args = {
    "owner": "avdel",
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
    "on_failure_callback": on_failure_callback,
}

with DAG(
    dag_id="telegram_alerts",
    default_args=default_args,
    start_date=datetime(2025, 12, 25),
    schedule_interval="15 3 * * *",
    catchup=True,
    max_active_runs=1,
) as dag:
    start, end = (EmptyOperator(task_id=task) for task in "start end".split())
    raise_exception_when_even = PythonOperator(
        task_id="raise_exception_when_even", python_callable=when_even_raise_exception
    )

    start >> raise_exception_when_even >> end

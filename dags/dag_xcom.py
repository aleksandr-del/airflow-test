from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from function import pull_conn_id, push_conn_id

default_args = {"owner": "avdel", "retries": 1, "retry_delays": timedelta(seconds=5)}


with DAG(
    dag_id="xcom",
    default_args=default_args,
    start_date=datetime(2026, 1, 12),
    schedule_interval="@once",
    tags=["push", "pull", "xcom"],
) as dag:
    start, end = (EmptyOperator(task_id=task) for task in "start end".split())
    push_xcom = PythonOperator(
        task_id="push_xcom",
        python_callable=push_conn_id,
        op_kwargs={"conn_id": "{{ var.value.duckdb_conn_id }}"},
    )
    pull_xcom = PythonOperator(task_id="pull_xcom", python_callable=pull_conn_id)

    start >> push_xcom >> pull_xcom >> end

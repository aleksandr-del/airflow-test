from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.http.operators.http import HttpOperator

default_args = {"owner": "avdel", "retries": 1, "retry_delays": timedelta(seconds=5)}

with DAG(
    dag_id="http_get",
    default_args=default_args,
    start_date=datetime(2026, 1, 12),
    schedule_interval="@once",
    tags=["get", "get"],
) as dag:
    start, end = (EmptyOperator(task_id=task) for task in "start end".split())
    get = HttpOperator(
        task_id="get",
        http_conn_id="exchange_rate_conn_id",
        endpoint="timeframe",
        method="GET",
        data={
            "access_key": "{{ var.value.exchangerate_access_key }}",
            "source": "USD",
            "start_date": "{{ ds }}",
            "end_date": "{{ ds }}",
        },
        response_filter=lambda response: response.json()["quotes"][
            list(response.json()["quotes"].keys())[0]
        ]["USDRUB"],
    )

    start >> get >> end

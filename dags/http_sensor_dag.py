from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.http.sensors.http import HttpSensor

default_args = {"owner": "avdel", "retries": 1, "retry_delays": timedelta(seconds=3)}

with DAG(
    dag_id="http_sensor",
    default_args=default_args,
    start_date=datetime(2026, 1, 13),
    schedule_interval="@once",
    tags=["http", "sensor", "api"],
) as dag:
    start, end = (EmptyOperator(task_id=task) for task in "start end".split())
    is_five = HttpSensor(
        task_id="is_five",
        http_conn_id="random_int_conn_id",
        endpoint="integers",
        method="GET",
        request_params={
            "num": "1",
            "min": "1",
            "max": "10",
            "col": "1",
            "base": "10",
            "format": "plain",
            "rnd": "new",
        },
        mode="poke",
        poke_interval=timedelta(seconds=3),
        timeout=timedelta(minutes=10),
        response_check=lambda response: response.json() == 5,
    )

    start >> is_five >> end

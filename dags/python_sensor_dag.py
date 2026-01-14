from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.sensors.python import PythonSensor
from function import sensor_file

default_args = {"owner": "avdel", "retries": 1, "retry_delays": timedelta(seconds=3)}

with DAG(
    dag_id="sensor_file",
    default_args=default_args,
    start_date=datetime(2026, 1, 13),
    schedule_interval="@once",
    tags=["python", "sensor", "file"],
) as dag:
    start, end = (EmptyOperator(task_id=task) for task in "start end".split())
    check_if_exists = PythonSensor(
        task_id="check_if_exists",
        python_callable=sensor_file,
        op_kwargs={"filename": "sensor_me.txt"},
        mode="reschedule",
        poke_interval=timedelta(minutes=10),
        timeout=timedelta(hours=1),
        soft_fail=True,
    )

    start >> check_if_exists >> end

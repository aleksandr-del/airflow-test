from datetime import date, datetime, timedelta
from typing import Any

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

default_args: dict[str, Any] = {
    "owner": "avdel",
    "retries": 1,
    "retry_delay": timedelta(seconds=3),
}

with DAG(
    dag_id="dynamic_dag",
    default_args=default_args,
    start_date=datetime(2026, 1, 13),
    schedule_interval="@once",
    tags=["dynamic", "tasks"],
) as dag:
    start, end = (EmptyOperator(task_id=task) for task in "start end".split())

    start_date: date = date(2026, 1, 9)
    end_date: date = date(2026, 1, 14)
    delta = end_date - start_date
    dates: list[str] = [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(delta.days + 1)
    ]
    tasks: list = []

    for date in dates:
        task = BashOperator(
            task_id=f"task_{date.replace('-', '_')}",
            bash_command=f'echo "SELECT * FROM TABLE WHERE loaded_at = \'{date}\'"',
            env={"date": date},
        )
        tasks.append(task)

        chain(start, tasks, end)

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# from airflow.utils.dates import days_ago
from function import failing_function, function

default_args: dict = {
    "owner": "avdel",
    "retries": 3,
    "retry_delay": timedelta(seconds=5),
}

with DAG(
    dag_id="test_dag",
    default_args=default_args,
    start_date=datetime(2026, 1, 11),
    schedule_interval=timedelta(days=1),
    tags=["test"],
) as dag:
    start, end = [EmptyOperator(task_id=task) for task in "start end".split()]

    task_1 = PythonOperator(
        task_id="task_1",
        python_callable=function,
        op_kwargs={
            "x": 3,
            "y": 5,
        },
        trigger_rule="all_done",
    )

    task_2 = BashOperator(
        task_id="task_2",
        bash_command='echo "Text: $text"',
        env={"text": "{{ dag_run }}"},
        trigger_rule="all_done",
    )

    failing_task = PythonOperator(
        task_id="failing_task",
        python_callable=failing_function,
    )

    start >> failing_task >> [task_1, task_2] >> end

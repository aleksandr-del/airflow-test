#!/usr/bin/env python3

from pathlib import Path

from airflow.exceptions import AirflowException
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.utils.context import Context
from pendulum import DateTime


def function(x: int, y: int, **context: Context) -> int:
    logger = context["ti"].log
    logger.info("Execution date %s", context["ds"])
    result: int = x + y
    logger.info("%s + %s = %s", x, y, result)

    return result


def failing_function() -> int | float | None:
    return 1 / 0


def print_context(**context: Context) -> None:
    logger = context["ti"].log
    logger.info("Execution date: %s", context["execution_date"])
    logger.info("Start date: %s", context["ds"])


def push_conn_id(conn_id: str, **context: Context) -> None:
    context["ti"].xcom_push(key="local_path", value=conn_id)
    context["ti"].log.info("Saved conn_id for duckdb in xcom")


def pull_conn_id(**context: Context) -> None:
    conn_id: str = context["ti"].xcom_pull(task_ids="push_xcom", key="local_path")
    context["ti"].log.info("Pulled local path: %s", conn_id)


def get_even_or_odd_day(**context: Context) -> str:
    dt: DateTime = context["logical_date"]
    return "even" if dt.day % 2 == 0 else "odd"


def get_even(**context: Context) -> bool:
    dt: DateTime = context["logical_date"]
    return dt.day % 2 == 0


def sensor_file(filename: str) -> bool:
    cwd = Path(".")
    file_to_sensor = cwd / filename
    return file_to_sensor.exists()


def when_even_raise_exception(**context: Context) -> None:
    dt: DateTime = context["logical_date"]
    if dt.day % 2 == 0:
        raise AirflowException(
            (f"Today is {context['ds']}. {dt.day} is an even number.")
        )


def on_failure_callback(context: Context) -> None:
    text = f"""
    Task failed!

    DAG: {context["dag"].dag_id}
    Task: {context["task_instance"].task_id}
    Time: {context["execution_date"]}
    Error: {str(context["exception"])[:3000]}
    """
    send_message = TelegramOperator(
        task_id="alerting", telegram_conn_id="telegram_conn_id", text=text
    )
    return send_message.execute(context=context)

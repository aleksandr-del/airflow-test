#!/usr/bin/env python3

from typing import Any


def function(x: int, y: int, **context: dict[str, Any]) -> int:
    logger = context["ti"].log
    logger.info("Execution date %s", context["ds"])
    result: int = x + y
    logger.info("%s + %s = %s", x, y, result)

    return result


def failing_function() -> int | float | None:
    return 1 / 0


def print_context(**context) -> None:
    logger = context["ti"].log
    logger.info("Execution date: %s", context["execution_date"])
    logger.info("Start date: %s", context["ds"])


def push_conn_id(conn_id: str, **context: dict[str, Any]) -> None:
    context["ti"].xcom_push(key="local_path", value=conn_id)
    context["ti"].log.info("Saved conn_id for duckdb in xcom")


def pull_conn_id(**context: dict[str, Any]) -> None:
    conn_id = context["ti"].xcom_pull(task_ids="push_xcom", key="local_path")
    context["ti"].log.info("Pulled local path: %s", conn_id)


def get_even_or_odd_day(**context: dict[str, Any]) -> str:
    dt = context["logical_date"]
    return "even" if dt.day % 2 == 0 else "odd"


def get_even(**context: dict[str, Any]) -> bool:
    dt = context["logical_date"]
    return dt.day % 2 == 0

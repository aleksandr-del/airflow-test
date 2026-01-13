from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from customoperator import DuckDBCustomOperator

default_args = {"owner": "avdel", "retries": 1, "retry_delays": timedelta(seconds=5)}

with DAG(
    dag_id="duckdb",
    default_args=default_args,
    start_date=datetime(2026, 1, 12),
    schedule_interval="@once",
    tags=["sql", "duckdb"],
) as dag:
    start, end = (EmptyOperator(task_id=task) for task in "start end".split())
    sql_query = DuckDBCustomOperator(
        task_id="sql_query",
        local_duckdb_conn_id="duckdb_conn_id",
        query="query.sql",
        params={
            "departments": ["bed", "living", "dining"],
            "table_name": "analytics.int_orders_items_products_joined",
        },
    )

    start >> sql_query >> end

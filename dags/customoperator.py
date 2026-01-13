from airflow.models import BaseOperator
from airflow.utils.context import Context
from duckdb_provider.hooks.duckdb_hook import DuckDBHook


class DuckDBCustomOperator(BaseOperator):
    template_fields = ["query", "local_duckdb_conn_id"]
    template_ext = ["sql"]

    def __init__(self, local_duckdb_conn_id: str, query: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.local_duckdb_conn_id = local_duckdb_conn_id
        self.query = query

    def execute(self, context: Context) -> None:
        duckdb_hook = DuckDBHook(self.local_duckdb_conn_id)
        with duckdb_hook.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.query)
                col_names = [col[0] for col in cursor.description]
                self.log.info("Column names: %s", col_names)
                rows = cursor.fetchall()
                data = [dict(zip(col_names, row)) for row in rows]
                self.log.info("Retrieved data: %s", data)

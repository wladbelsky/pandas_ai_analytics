import duckdb
import pandas as pd


def execute_query(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    Выполняет SQL-запрос над pandas.DataFrame с помощью duckdb.
    Затем форматирует результат для вывода.
    """
    try:
        # Выполнение SQL-запроса с помощью DuckDB
        con = duckdb.connect()
        try:
            con.register("data", df)

            result_df = con.execute(query).fetchdf()

            return result_df
        finally:
            con.close()
    except Exception as e:
        raise RuntimeError(f"Ошибка при выполнении запроса: {e}") from e

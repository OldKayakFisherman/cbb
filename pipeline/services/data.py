from contextlib import contextmanager
from collections.abc import Generator
from datetime import datetime
from psycopg2.extensions import cursor, connection
from psycopg2.extras import execute_values
from psycopg2.pool import SimpleConnectionPool
from services.config import AppSettings
from services.utilities import getDuration

config = AppSettings()

DEFAULT_EXECUTION_PAGE_SIZE=1000

PG_USER = config.db_user
PG_DATABASE = config.database
PG_HOST = config.db_host
PG_PORT = config.db_port
PG_SCHEMA = config.db_schema
PG_PASSWORD = config.db_password

# pool defined with 15 connections
connection_pool = SimpleConnectionPool(1, 15, user=PG_USER, database=PG_DATABASE, password=PG_PASSWORD,
                                       host=PG_HOST, port=PG_PORT, options=f"-c search_path={PG_SCHEMA}")

@contextmanager
def get_cursor() -> Generator[cursor]:
    con: connection = connection_pool.getconn()
    try:
        yield con.cursor()
    finally:
        con.commit()
        connection_pool.putconn(con)


class PipelineRepository:

    def purge(self):

        with get_cursor() as cur:
            cur.execute("DELETE FROM pipeline_runs")

    def stamp_run(self, run_date: datetime):

        prms = (run_date, )

        sql = "INSERT INTO pipeline_runs (run_date) values (%s)"

        with get_cursor() as cur:
            cur.execute(sql, prms)


    def run_needed(self, target_hours: int):

        result: bool = True

        sql = "SELECT MAX(run_date) FROM pipeline_runs"

        with get_cursor() as cur:
            cur.execute(sql)
            last_run = cur.fetchone()[0]

        if last_run:
            actual_hours = getDuration(last_run, interval="hours")
            if actual_hours > target_hours:
                result = True

        return result
    
class IngestionRepository:

    def log_run(self, pipeline: str, record_imported: int, api_url: str) -> None:

        sql = f"""
            INSERT INTO ingestion_log
            (
                pipeline, records_imported, api_url
            )
            VALUES %s
        """

        prms = [(pipeline, record_imported, api_url)]

        with get_cursor() as cur:
            cur.execute(sql, prms)
        

class CBPCountyRepository:

    def purge(self):

        with get_cursor() as cur:
            cur.execute("DELETE FROM cbp_county")


    def save(self, records: list[dict], year: int):

        sql = """
                INSERT INTO cbp_county
                (
                        GEO_ID,ESTAB,PAYANN,PAYQTR1,EMP,NAICS,STATE,COUNTY
                )
                values %s
        """

        prms = []

        for record in records[1:]:
            prms.append((record[0], record[1], record[2],record[3],record[4],
                              record[5],record[6], record[7]))

        with get_cursor() as cur:
            try:
                execute_values(cur, sql, prms, page_size=DEFAULT_EXECUTION_PAGE_SIZE)
            except Exception as ex:
                print(ex)


class CBPStateRepository:

    def purge(self):

        with get_cursor() as cur:
            cur.execute("DELETE FROM cbp_county")


    def save(self, records: list[dict], year: int):

        sql = """
                INSERT INTO cbp_county
                (
                        GEO_ID,ESTAB,PAYANN,PAYQTR1,EMP,NAICS,STATE,COUNTY
                )
                values %s
        """

        prms = []

        for record in records[1:]:
            prms.append((record[0], record[1], record[2],record[3],record[4],
                              record[5],record[6], record[7]))


        with get_cursor() as cur:
            execute_values(cur, sql, prms, page_size=DEFAULT_EXECUTION_PAGE_SIZE)

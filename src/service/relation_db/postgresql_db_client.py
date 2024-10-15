import os
from typing import Any, List, Dict

import psycopg
from psycopg.rows import dict_row

from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.sql_client_interface import SQLClientInterface


def get_conn_uri():
    user_id = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    postgres_db = os.environ['POSTGRES_DB']
    postgres_host = os.environ['LOCALHOST']

    conn_str = f"host={postgres_host} port=5432 dbname={postgres_db} user={user_id} password={password} connect_timeout=10"
    return conn_str


class PostgreSQLClient(SQLClientInterface):
    def __init__(self):
        self._conn_uri = get_conn_uri()

    def sync_db_ops(self, sql_syntax: str, fetch_type: FetchType = FetchType.Idle,
                    parameters: list[Any] = None) -> List | Dict | None:
        if parameters is None:
            parameters = []

        with psycopg.connect(self._conn_uri, row_factory=dict_row) as aconn:
            with aconn.cursor() as acur:
                acur.execute(sql_syntax, parameters)

                if fetch_type == FetchType.Many:
                    fetch_r = acur.fetchall()
                if fetch_type == FetchType.One:
                    fetch_r = acur.fetchone()

                if fetch_type != FetchType.Idle:
                    return fetch_r

    async def async_db_ops(self, sql_syntax: str, fetch_type: FetchType = FetchType.Idle,
                           parameters: list[Any] = None) -> List | Dict | None:
        if parameters is None:
            parameters = []

        async with await psycopg.AsyncConnection.connect(self._conn_uri, row_factory=dict_row) as aconn:
            async with aconn.cursor() as acur:
                await acur.execute(sql_syntax, parameters)

                if fetch_type == FetchType.Many:
                    fetch_r = await acur.fetchall()
                if fetch_type == FetchType.One:
                    fetch_r = await acur.fetchone()

                if fetch_type != FetchType.Idle:
                    return fetch_r

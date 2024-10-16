from typing import Any, List, Dict

from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.sql_client_interface import SQLClientInterface


class DummySQLClient(SQLClientInterface):
    def sync_db_ops(self, sql_syntax: str, fetch_type: FetchType = FetchType.Idle,
                    parameters: list[Any] = None) -> List | Dict | None:
        pass

    async def async_db_ops(self, sql_syntax: str, fetch_type: FetchType = FetchType.Idle,
                           parameters: list[Any] = None) -> List | Dict | None:
        pass
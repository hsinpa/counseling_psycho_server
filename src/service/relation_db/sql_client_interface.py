from abc import ABC, abstractmethod
from typing import Any, List, Dict

from src.service.relation_db.postgres_db_manager import FetchType


class SQLClientInterface(ABC):

    @abstractmethod
    def sync_db_ops(self, sql_syntax: str, fetch_type: FetchType = FetchType.Idle, parameters: list[Any] = None) -> List | Dict | None:
        pass

    @abstractmethod
    async def async_db_ops(self, sql_syntax: str, fetch_type: FetchType = FetchType.Idle, parameters: list[Any] = None)-> List | Dict | None:
        pass
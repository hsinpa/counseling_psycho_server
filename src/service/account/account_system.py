from enum import Enum

from src.service.relation_db.postgres_db_static import DB_TABLE_ACCOUNT
from src.service.relation_db.postgresql_db_client import PostgreSQLClient

class LoginType(str, Enum):
    SelfHost='self_host'

class AccountSystem:

    def __init__(self, sql_client: PostgreSQLClient):
        self._sql_client = sql_client

    async def login(self, email:str, password: str):
        pass

    async def register_account(self, username: str, email: str, password: str):
        sql_syntax = f"""INSERT INTO {DB_TABLE_ACCOUNT} (username, email, password_hash, login_type) 
                        VALUES(%s, %s, %s, %s)"""


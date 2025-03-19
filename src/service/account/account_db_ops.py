from src.model.account_model import LoginType
from src.service.relation_db.postgres_db_manager import FetchType
from src.service.relation_db.postgres_db_static import DB_TABLE_ACCOUNT
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.utility.crypto.password_handler import generate_auth_token, generate_refresh_token


class AccountDBOps:

    def __init__(self, sql_client: PostgreSQLClient):
        self._sql_client = sql_client

    def issue_token(self, email: str):
        auth_payload, auth_token = generate_auth_token(email)
        refresh_payload, refresh_token = generate_refresh_token(email)

        return {'auth_token': auth_token, 'refresh_token': refresh_token,
                'auth_expire_date': auth_payload['exp'], 'refresh_expire_date': refresh_payload['exp'] }

    async def is_email_exist(self, email: str) -> bool:
        sql_syntax = f'SELECT COUNT(email) as email_count FROM {DB_TABLE_ACCOUNT} WHERE email=%s;'
        sql_result = await self._sql_client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[email])

        return sql_result['email_count'] > 0

    async def get_account(self, email: str):
        sql_syntax = f'SELECT email, password_hash, login_type, username FROM {DB_TABLE_ACCOUNT} WHERE email=%s;'
        return await self._sql_client.async_db_ops(sql_syntax=sql_syntax, fetch_type=FetchType.One, parameters=[email])

    async def append_account(self, username: str, email: str, password: str, login_type: LoginType):
        sql_syntax = f"""INSERT INTO {DB_TABLE_ACCOUNT} (username, email, password_hash, login_type) VALUES(%s, %s, %s, %s)"""

        await self._sql_client.async_db_ops(sql_syntax=sql_syntax, parameters=[username, email, password, login_type])
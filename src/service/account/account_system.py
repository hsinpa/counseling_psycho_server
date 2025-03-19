from src.model.account_model import LoginType, AccountAuthResp
from src.service.account.account_db_ops import AccountDBOps
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.utility.crypto.password_handler import encode_password, verify_password, verify_token
from src.utility.utility_method import is_valid_email


class AccountSystem:

    def __init__(self, sql_client: PostgreSQLClient):
        self._sql_client = sql_client
        self._db_ops = AccountDBOps(sql_client=sql_client)

    async def login(self, email: str, password: str):
        if is_valid_email(email) is False:
            raise ValueError(f'Address {email} is not a valid email')

        account_info: dict = await self._db_ops.get_account(email)
        if verify_password(password, account_info['password_hash']) is False:
            raise ValueError(f'Password no match')

        issue_token_info = self._db_ops.issue_token(email)

        return AccountAuthResp(**issue_token_info, username=account_info['username'],
                               email=email, login_type=LoginType.SelfHost)

    async def register(self, username: str, email: str, password: str):
        if is_valid_email(email) is False:
            raise ValueError(f'Address {email} is not a valid email')

        if await self._db_ops.is_email_exist(email):
            raise ValueError(f'Email {email} already exists')

        hash_password = encode_password(password)

        await self._db_ops.append_account(username, email, hash_password, LoginType.SelfHost)
        issue_token_info = self._db_ops.issue_token(email)

        return AccountAuthResp(**issue_token_info, username=username,
                               email=email, login_type=LoginType.SelfHost)

    def refresh_token(self, email: str, refresh_token: str):
        if verify_token(refresh_token):
            return self._db_ops.issue_token(email)
        return None
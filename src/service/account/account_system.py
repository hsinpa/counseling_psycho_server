
from src.model.account_model import LoginType, AccountReturnResp, AccountAuthModel
from src.service.account.account_db_ops import AccountDBOps
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.utility.crypto.password_handler import encode_password, verify_password, verify_token
from src.utility.utility_method import is_valid_email
from fastapi import HTTPException


class AccountSystem:

    def __init__(self, sql_client: PostgreSQLClient):
        self._sql_client = sql_client
        self._db_ops = AccountDBOps(sql_client=sql_client)

    async def login(self, email: str, password: str) -> AccountReturnResp:
        account_info: dict = await self._db_ops.get_account(email)

        if is_valid_email(email) is False or account_info is None:
            raise HTTPException(status_code=404,detail=f'Address {email} is not a valid email')

        if verify_password(password, account_info['password_hash']) is False:
            raise HTTPException(status_code=404,detail=f'Password no match')

        issue_token_info = self._db_ops.issue_token(email)

        return AccountReturnResp(**issue_token_info, username=account_info['username'],
                                 email=email, login_type=LoginType.SelfHost)

    async def register(self, username: str, email: str, password: str) -> AccountReturnResp:
        if is_valid_email(email) is False:
            raise HTTPException(status_code=404,detail=f'Address {email} is not a valid email')

        if await self._db_ops.is_email_exist(email):
            raise HTTPException(status_code=404,detail=f'Email {email} already exists')

        hash_password = encode_password(password)

        await self._db_ops.append_account(username, email, hash_password, LoginType.SelfHost)
        issue_token_info = self._db_ops.issue_token(email)

        return AccountReturnResp(**issue_token_info, username=username,
                                 email=email, login_type=LoginType.SelfHost)

    def refresh_token(self, email: str, refresh_token: str) -> AccountAuthModel:
        if verify_token(refresh_token):
            return AccountAuthModel(**self._db_ops.issue_token(email))
        raise ValueError(f'Refresh token on email {email} FAILED')
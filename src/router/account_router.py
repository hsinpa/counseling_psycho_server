import asyncio
from fastapi import APIRouter, UploadFile, File, Form

from src.model.account_model import AccountRegisterModel, AccountReturnResp, AccountSelfLoginModel, AccountTokenModel, \
    AccountAuthModel
from src.service.account.account_system import AccountSystem
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.utility.crypto.password_handler import generate_auth_token, verify_token

router = APIRouter(prefix="/api/account", tags=["Account"])

@router.post("/account_self_login")
async def account_login(input_params: AccountSelfLoginModel) -> AccountReturnResp:
    account_system = AccountSystem(sql_client=PostgreSQLClient())
    return await account_system.login(input_params.email, input_params.password)

@router.post("/account_register")
async def account_register(input_params: AccountRegisterModel):
    account_system = AccountSystem(sql_client=PostgreSQLClient())

    register_result = await account_system.register(input_params.username, input_params.email, input_params.password)

    return register_result

@router.post("/refresh_auth")
async def account_refresh_auth(input_params: AccountTokenModel) -> AccountAuthModel:
    account_system = AccountSystem(sql_client=PostgreSQLClient())

    return account_system.refresh_token(input_params.email, input_params.token)
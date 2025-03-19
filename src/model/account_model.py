import datetime
from enum import Enum
from pydantic import BaseModel, Field

class LoginType(str, Enum):
    SelfHost='self_host'

class AccountRegisterModel(BaseModel):
    username: str
    password: str
    email: str
    login_type: LoginType

class AccountSelfLoginModel(BaseModel):
    email: str
    password: str

class AccountTokenModel(BaseModel):
    email: str
    token: str

class AccountAuthResp(BaseModel):
    username: str
    email: str
    login_type: LoginType

    auth_token: str
    refresh_token: str

    auth_expire_date: datetime.datetime = Field(..., description='UTC 1 hour')
    refresh_expire_date: datetime.datetime = Field(..., description='UTC 7 days')
    status: int = Field(default=200, description='Account status')
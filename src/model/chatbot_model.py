# Router Model
from pydantic import BaseModel


class ChatbotUserInputType(BaseModel):
    input: str
    user_id: str
    session_id: str

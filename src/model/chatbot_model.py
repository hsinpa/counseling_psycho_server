# Router Model
from typing import Optional

from pydantic import BaseModel, Field


class ChatbotUserInputType(BaseModel):
    text: str
    user_id: str
    session_id: str

    # Only used in streaming
    websocket_id: Optional[str] = None
    token: Optional[str] = None
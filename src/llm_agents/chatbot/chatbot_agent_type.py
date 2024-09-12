from typing import TypedDict, Annotated, Any

from pydantic import BaseModel, Field

from src.model.general_model import StreamingDataChunkType

def annotate_list(x: list[Any], y: list[Any]):
    if x is None:
        x = []

    x.extend(y)
    return x


class ChatbotAgentState(TypedDict):
    final_message: Annotated[list[StreamingDataChunkType], annotate_list]
    scenario: Annotated[str, lambda x, y: y]
    query: str
    chatbot_id: str
    chatroom_id: int
    kg_triples: list[str]
    new_chatroom_summary: str


class KGRetrieveType(BaseModel):
    thought: str = Field(..., description='仔細思考 "使用者回覆" 中的訊息和其中想要表達的意思')
    triple: list[str] = Field(..., description='內容類似Cypher語法, 由標籤, 關係 和 標籤 組成. Ex, Thomas | 朋友 | Thomas')
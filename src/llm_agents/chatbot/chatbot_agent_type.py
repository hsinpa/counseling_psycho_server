from typing import TypedDict, Annotated, Any, Optional

from pydantic import BaseModel, Field

from src.model.general_model import StreamingDataChunkType


def annotate_list(x: list[Any], y: list[Any]):
    if x is None:
        x = []

    x.extend(y)
    return x


class KGRetrieveType(BaseModel):
    thought: str = Field(..., description='仔細思考 "使用者回覆" 中的訊息和其中想要表達的意思')
    triple: list[str] = Field(...,
                              description='內容類似Cypher語法, 由標籤, 關係 和 標籤 組成. Ex, Thomas | 朋友 | Thomas')


class TripleType(BaseModel):
    uuid: str
    host_node: str
    relation: str
    child_node: str
    embedding: Optional[list[float]] = Field(default=[])


class ChatbotAgentState(TypedDict):
    query: str
    long_term_plan: str
    summary: str
    output: str

    kg_triples: list[TripleType]  # Convert from User Input
    retrieve_triples: list[TripleType]  # Get from VectorDB by kg_triples

from enum import Enum
from typing import TypedDict

from pydantic import BaseModel


class DataChunkType(Enum):
    Chunk = 'chunk'
    Complete = 'complete'


class StreamingDataChunkType(BaseModel):
    session_id: str
    data: str
    type: DataChunkType

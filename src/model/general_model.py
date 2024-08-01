from enum import Enum
from typing import TypedDict

from pydantic import BaseModel

class SocketEvent:
    open = 'socket_open'
    bot = 'bot'


class DataChunkType(str, Enum):
    Chunk = 'chunk'
    Complete = 'complete'


class StreamingDataChunkType(BaseModel):
    session_id: str
    data: str
    type: DataChunkType

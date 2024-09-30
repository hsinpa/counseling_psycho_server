from enum import Enum
from typing import TypedDict

from pydantic import BaseModel

class SocketEvent:
    open = 'socket_open'
    bot = 'bot'
    message_stream = 'main_content_socket'


class DataChunkType(str, Enum):
    Chunk = 'chunk'
    Complete = 'complete'


class StreamingDataChunkType(BaseModel):
    bubble_id: str
    session_id: str
    data: str
    type: DataChunkType
    index: int

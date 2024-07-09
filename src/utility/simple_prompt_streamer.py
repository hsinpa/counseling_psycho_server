from typing import Any

from langchain_core.runnables import RunnableSerializable

from src.model.general_model import StreamingDataChunkType, DataChunkType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.websocket.websocket_manager import websocket_manager


class SimplePromptStreamer:
    def __init__(self, user_id: str, session_id: str):
        self._user_id = user_id
        self._session_id = session_id

    async def execute(self, chain: RunnableSerializable[dict, Any], p_input: dict = {}):
        results = ''

        async for chunk in chain.astream(p_input):
            stream_data = StreamingDataChunkType(session_id=self._session_id, data=chunk, type=DataChunkType.Chunk)
            websocket_manager.send(target_id=self._user_id, data=stream_data.model_dump_json())
            results = results + chunk

        stream_data = StreamingDataChunkType(session_id=self._session_id, data=results, type=DataChunkType.Complete)
        websocket_manager.send(target_id=self._user_id, data=stream_data.model_dump_json())

        return results

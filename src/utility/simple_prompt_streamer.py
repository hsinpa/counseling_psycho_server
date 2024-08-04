import json
from typing import Any

from langchain_core.runnables import RunnableSerializable

from src.model.general_model import StreamingDataChunkType, DataChunkType, SocketEvent
from src.websocket.websocket_manager import websocket_manager


class SimplePromptStreamer:
    def __init__(self, user_id: str, session_id: str):
        self._user_id = user_id
        self._session_id = session_id

    async def execute(self, chain: RunnableSerializable[dict, Any], p_input: dict = {}):
        results = ''

        async for chunk in chain.astream(p_input):
            data_chunk = str(chunk)

            stream_data = StreamingDataChunkType(session_id=self._session_id, data=data_chunk, type=DataChunkType.Chunk)
            json_string = {'event': SocketEvent.bot, **stream_data.model_dump()}

            await websocket_manager.send(target_id=self._user_id, data=json.dumps(json_string, ensure_ascii=False))
            results = results + data_chunk

        stream_data = StreamingDataChunkType(session_id=self._session_id, data=results, type=DataChunkType.Complete)
        json_string = {'event': SocketEvent.bot, **stream_data.model_dump()}

        await websocket_manager.send(target_id=self._user_id, data=json.dumps(json_string, ensure_ascii=False))

        return results

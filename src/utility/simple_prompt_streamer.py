import json
import uuid
from typing import Any

from langchain_core.runnables import RunnableSerializable

from src.model.general_model import StreamingDataChunkType, DataChunkType
from src.websocket.websocket_manager import get_websocket


class SimplePromptStreamer:
    def __init__(self, session_id: str, socket_id: str, event_tag: str):
        self._session_id = session_id
        self._socket_id = socket_id
        self._event_tag = event_tag
        self._websocket_manager = get_websocket()

    async def execute(self, chain: RunnableSerializable[dict, Any], p_input: dict = {}):
        results = ''
        bubble_id = str(uuid.uuid4())
        index = 0

        stream_data = StreamingDataChunkType(bubble_id=bubble_id, session_id=self._session_id, data=results,
                                             type=DataChunkType.Chunk, index=index)

        async for chunk in chain.astream(p_input):
            data_chunk = str(chunk)

            stream_data.data = data_chunk
            stream_data.index = index

            json_string = {'event': self._event_tag, **stream_data.model_dump()}
            await self._websocket_manager.send(target_id=self._socket_id, data=json.dumps(json_string, ensure_ascii=False))
            results = results + data_chunk

            index += 1

        stream_data.type = DataChunkType.Complete
        stream_data.data = results
        json_string = {'event': self._event_tag, **stream_data.model_dump()}

        await self._websocket_manager.send(target_id=self._socket_id, data=json.dumps(json_string, ensure_ascii=False))

        return results

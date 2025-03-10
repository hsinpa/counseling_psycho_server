from abc import ABC


class StreamingInterface(ABC):
    async def queue_message(self, stream_id: str, data: str):
        pass
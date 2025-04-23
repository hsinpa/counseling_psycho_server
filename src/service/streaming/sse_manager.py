import asyncio
from fastapi import Request
from src.service.streaming.streaming_interface import StreamingInterface


class SSEResponseManager(StreamingInterface):
    def __init__(self):
        self._sse_dict = {}

    async def queue_message(self, sse_id: str, data: str):
        q: asyncio.Queue = self.get_sse_queue(sse_id)
        await q.put(data)

    def get_sse_queue(self, sse_id: str):
        if sse_id not in self._sse_dict or self._sse_dict[sse_id] is None:
            self._sse_dict[sse_id] = asyncio.Queue()

        return self._sse_dict[sse_id]

    async def process_event_loop(self, sse_id: str, request: Request):
        queue = self.get_sse_queue(sse_id)

        while True:
            try:
                message = await asyncio.wait_for(queue.get(), timeout=10)
                yield f"data: {message}\n\n"

            except asyncio.TimeoutError:
                # Send a heartbeat to keep the connection alive
                yield f": heartbeat\n\n"

            finally:
                if await request.is_disconnected():
                    self._sse_dict.pop(sse_id, None)
                    print(f'{sse_id} Exist')


sse_manager = SSEResponseManager()

def get_sse():
    return sse_manager
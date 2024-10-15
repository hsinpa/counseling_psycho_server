import asyncio
import typing

from fastapi import WebSocket


class WebSocketManager:
    __instance = None
    blocked_id_set: set[str] = set()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(WebSocketManager, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.active_connections: typing.Dict[str, WebSocket] = {}

    async def send(self, target_id: str, data: str):
        if target_id in self.active_connections:
            await self.active_connections[target_id].send_text(data)

    async def connect(self, socket_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[socket_id] = websocket

    def disconnect(self, socket_id: str):
        if socket_id in self.active_connections:
            del self.active_connections[socket_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    def register_block_id(self, block_id: str):
        if block_id in self.blocked_id_set:
            return False
        self.blocked_id_set.add(block_id)
        return True

    def deregister_block_id(self, block_id: str):
        self.blocked_id_set.remove(block_id)


websocket_manager = WebSocketManager()


def get_websocket():
    return websocket_manager

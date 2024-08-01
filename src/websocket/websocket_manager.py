import asyncio
import typing

from fastapi import WebSocket


class WebSocketManager:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(WebSocketManager, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.active_connections: typing.Dict[str, WebSocket] = {}

    async def send(self, target_id: str, data: str):
        if target_id in self.active_connections:
            await self.active_connections[target_id].send_text(data)

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


websocket_manager = WebSocketManager()


def get_websocket():
    return websocket_manager

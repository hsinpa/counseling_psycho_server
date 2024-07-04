import asyncio

from websockets import WebSocketServerProtocol, serve


class WebSocketManager:
    async def set_up(self):
        async with serve(self.on_connect, "localhost", 8765):
            await asyncio.Future()  # run forever

    async def on_connect(self, socket: WebSocketServerProtocol):
        print('new socket ' + str(socket.id))

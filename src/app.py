import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.router.questionnaire_router import router as questionnaire_router
from src.websocket.websocket_manager import WebSocketManager

load_dotenv()
websocket_manager = WebSocketManager()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")
app.include_router(questionnaire_router)

@app.get("/")
async def root():
    return {"version": "0.0.2"}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id, websocket)

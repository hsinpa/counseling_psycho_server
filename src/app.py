import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.router.questionnaire_router import router as questionnaire_router
from src.router.multi_theory_router import router as multi_theory_router

from src.websocket.websocket_manager import  websocket_manager

load_dotenv()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")
app.include_router(questionnaire_router)
app.include_router(multi_theory_router)

@app.get("/")
async def root():
    return {"version": "0.0.2"}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(client_id, websocket)
    try:
       await websocket.send_text('HOW ARE YOU')
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id, websocket)
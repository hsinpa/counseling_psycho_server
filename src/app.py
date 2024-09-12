import asyncio
import json
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.model.general_model import SocketEvent
from src.router.questionnaire_router import router as questionnaire_router
from src.router.multi_theory_router import router as multi_theory_router
from src.router.yuri_temp_router import router as yuri_router
from src.router.chatbot_router import router as chatbot_router

from fastapi.middleware.cors import CORSMiddleware
from src.websocket.websocket_manager import websocket_manager

load_dotenv()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")
app.include_router(questionnaire_router)
app.include_router(multi_theory_router)
app.include_router(yuri_router)
app.include_router(chatbot_router)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://counseling-psycho.vercel.app",
    "https://itri-mqtt-doll.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"version": "0.0.2"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    g_user_id = str(uuid.uuid4())

    await websocket_manager.connect(g_user_id, websocket)
    try:
        await websocket.send_text(json.dumps({'event': SocketEvent.open, '_id': g_user_id}))
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        print('websocket disconnect user '+g_user_id)
        websocket_manager.disconnect(g_user_id)

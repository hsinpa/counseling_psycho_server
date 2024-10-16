import asyncio
import json
import sys
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.model.general_model import SocketEvent
from src.router.questionnaire_router import router as questionnaire_router
from src.router.multi_theory_router import router as multi_theory_router
from src.router.yuri_temp_router import router as yuri_router
from src.router.chatbot_router import router as chatbot_router
from src.router.talk_simulation_router import router as talk_router

from fastapi.middleware.cors import CORSMiddleware

from src.service.vector_db.vector_db_manager import VectorDBManager
from src.websocket.websocket_manager import websocket_manager

load_dotenv()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")
app.include_router(questionnaire_router)
app.include_router(multi_theory_router)
app.include_router(yuri_router)
app.include_router(chatbot_router)
app.include_router(talk_router)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://counseling-psycho.vercel.app",
    "https://counseling-psycho-chatbot.vercel.app",
    "https://itri-mqtt-doll-git-dev-hsinpas-projects.vercel.app",
    "https://itri-mqtt-doll.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_db = VectorDBManager()
loop = asyncio.get_running_loop()
db_task = loop.create_task(vector_db.init_db_collection())

@app.get("/")
async def root():
    return {"version": "0.0.2"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    g_socket_id = str(uuid.uuid4())
    await websocket_manager.connect(g_socket_id, websocket)
    try:
        await websocket.send_text(json.dumps({'event': SocketEvent.open, '_id': g_socket_id}))
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        print('websocket disconnect user '+g_socket_id)
        websocket_manager.disconnect(g_socket_id)

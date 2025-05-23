import asyncio
import json
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import StreamingResponse

from src.model.general_model import SocketEvent
from src.router.supervisor_router import router as supervisor_router
from src.router.transcript_router import router as transcript_router
from src.router.account_router import router as account_router

from fastapi.middleware.cors import CORSMiddleware

from src.service.streaming.sse_manager import get_sse
from src.service.vector_db.vector_db_manager import VectorDBManager
from src.service.streaming.websocket_manager import websocket_manager

load_dotenv()

app = FastAPI(openapi_url="/docs/openapi.json", docs_url="/docs")
app.include_router(account_router)
app.include_router(supervisor_router)
app.include_router(transcript_router)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://counseling-psycho.vercel.app",
    "https://counseling-psycho-chatbot.vercel.app",
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


@app.get("/sse/{sse_id}")
async def sse_endpoint(sse_id: str, request: Request):
    """Endpoint that streams events to the client."""
    return StreamingResponse(get_sse().process_event_loop(sse_id, request), media_type="text/event-stream")
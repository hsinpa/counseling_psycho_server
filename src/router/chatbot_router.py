from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.llm_agents.chatbot.chatbot_manager import ChatbotManager
from src.llm_agents.chatbot.db_ops.chatbot_relation_db import get_chatroom_message
from src.model.chatbot_model import ChatbotUserInputType
from src.websocket.websocket_manager import get_websocket

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])
socket_manager = get_websocket()

@router.post("/chat")
async def chat(chat_input: ChatbotUserInputType):
    chatbot_manager = ChatbotManager(chat_input)

    r = await chatbot_manager.process_chat()

    return {'output': r['output']}

@router.post("/achat")
async def achat(chat_input: ChatbotUserInputType, background_tasks: BackgroundTasks):
    if chat_input.token is None:
        raise HTTPException(status_code=404, detail="Where is the Token")

    chatbot_manager = ChatbotManager(chat_input)

    background_tasks.add_task(chatbot_manager.process_chat)

    return {'token': chat_input.token}

@router.get('/message_history/user/{user_id}/session/{session_id}')
def get_message_history(user_id: str, session_id: str):
    chat_messages = get_chatroom_message(user_id, session_id, limit=30)

    return chat_messages


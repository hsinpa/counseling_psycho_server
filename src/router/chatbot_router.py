from fastapi import APIRouter

from src.llm_agents.chatbot.chatbot_manager import ChatbotManager
from src.model.chatbot_model import ChatbotUserInputType

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/chat")
async def chat(chat_input: ChatbotUserInputType):
    chatbot_manager = ChatbotManager(chat_input)

    r = await chatbot_manager.process_chat()
    return r

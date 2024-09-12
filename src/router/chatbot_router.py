import requests
from fastapi import APIRouter

from src.llm_agents.chatbot.chatbot_agent import ChatbotAgent
from src.model.chatbot_model import ChatbotUserInputType
from langfuse.callback import CallbackHandler

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/chat")
async def chat(chat_input: ChatbotUserInputType):
    chatbot_agent = ChatbotAgent(user_id=chat_input.user_id, session_id=chat_input.session_id, chat_summary='')

    compile_agent = chatbot_agent.create_graph().with_config({"callbacks": [CallbackHandler(user_id='hsinpa')]})

    r = await compile_agent.ainvoke({'query': chat_input.input})

    return r

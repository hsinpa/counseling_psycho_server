import asyncio
import uuid
from threading import Thread

from langchain.chains.question_answering.map_reduce_prompt import messages

from src.feature.chatbot.chatbot_agent import ChatbotAgent
from src.feature.chatbot.chatbot_agent_type import ChatbotAgentState
from src.feature.chatbot.db_ops.chatbot_relation_db import get_chatroom_info, get_chatroom_message
from src.feature.chatbot.post_ops.post_work_manager import PostWorkManager
from src.model.chatbot_model import ChatbotUserInputType
from langfuse.callback import CallbackHandler

from src.service.vector_db.vector_db_manager import VectorDBManager


class ChatbotManager:
    def __init__(self, chat_input: ChatbotUserInputType):
        self._chat_input = chat_input
        self._vector_db = VectorDBManager()

    async def process_chat(self) -> ChatbotAgentState:
        # Get Dat from DB
        chatroom_info = get_chatroom_info(self._chat_input.session_id)
        chat_messages = get_chatroom_message(self._chat_input.user_id, self._chat_input.session_id, limit=6)
        bubble_id = str(uuid.uuid4())

        # Agent
        chatbot_agent = ChatbotAgent(user_id=self._chat_input.user_id,
                                     session_id=self._chat_input.session_id,
                                     socket_id=self._chat_input.websocket_id,
                                     messages=chat_messages,
                                     vector_db=self._vector_db)

        compile_agent = chatbot_agent.create_graph()

        chat_result = await compile_agent.ainvoke(
            {
                'query': self._chat_input.text,
                'summary': chatroom_info.summary,
                'long_term_plan': chatroom_info.long_term_plan,
             }, config={"run_name": 'Chat Graph',
                  "callbacks": [CallbackHandler(
                      user_id='hsinpa',
                      session_id=self._chat_input.session_id
                  )]
            }
        )

        # Post work, no IO block
        post_agent = PostWorkManager(user_id=self._chat_input.user_id, session_id=self._chat_input.session_id,
                                     state=chat_result, messages=chat_messages)
        t = Thread(target=post_agent.exec_pipeline)
        t.start()

        return chat_result

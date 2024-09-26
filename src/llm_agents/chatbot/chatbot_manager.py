import asyncio
from threading import Thread

from src.llm_agents.chatbot.chatbot_agent import ChatbotAgent
from src.llm_agents.chatbot.post_ops.post_agent import PostAgent
from src.model.chatbot_model import ChatbotUserInputType
from langfuse.callback import CallbackHandler

from src.service.vector_db.vector_db_manager import VectorDBManager


class ChatbotManager:
    def __init__(self, chat_input: ChatbotUserInputType):
        self._chat_input = chat_input
        self._vector_db = VectorDBManager()

    async def process_chat(self):
        # todo: DB query
        chatbot_agent = ChatbotAgent(user_id=self._chat_input.user_id,
                                     session_id=self._chat_input.session_id,
                                     chat_summary='',
                                     vector_db=self._vector_db)

        compile_agent = chatbot_agent.create_graph()

        chat_result = await compile_agent.ainvoke({'query': self._chat_input.input},
                                           config={"run_name": 'Chat Graph',
                                               "callbacks": [CallbackHandler(
                                                   user_id='hsinpa',
                                                   session_id=self._chat_input.session_id
                                               )]})

        # Post work, no IO block
        post_agent = PostAgent(user_id=self._chat_input.user_id, session_id=self._chat_input.session_id,
                               state=chat_result, vector_db=self._vector_db)
        t = Thread(target=post_agent.exec_pipeline)
        t.start()

        return chat_result
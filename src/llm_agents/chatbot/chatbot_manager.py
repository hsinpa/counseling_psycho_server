from requests import session

from src.llm_agents.chatbot.chatbot_agent import ChatbotAgent
from src.model.chatbot_model import ChatbotUserInputType
from langfuse.callback import CallbackHandler


class ChatbotManager:
    def __init__(self, chat_input: ChatbotUserInputType):
        self._chat_input = chat_input

    async def process_chat(self):
        # todo: DB query
        chatbot_agent = ChatbotAgent(user_id=self._chat_input.user_id,
                                     session_id=self._chat_input.session_id,
                                     chat_summary='')

        compile_agent = chatbot_agent.create_graph()

        return await compile_agent.ainvoke({'query': self._chat_input.input},
                                           config={"run_name": 'Chat Graph',
                                               "callbacks": [CallbackHandler(
                                                   user_id='hsinpa',
                                                   session_id=self._chat_input.session_id
                                               )]})

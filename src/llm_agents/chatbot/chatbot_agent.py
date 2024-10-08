import json
import uuid
from typing import List

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.chatbot.chatbot_agent_type import ChatbotAgentState, KGRetrieveType, ChatMessage
from src.llm_agents.chatbot.chatbot_util import convert_triple_list_to_pydantic, convert_triple_list_to_string, \
    convert_triple_list_to_embedding, db_message_to_prompt
from src.llm_agents.chatbot.db_ops.chatbot_vector_db import retrieve_relate_triples
from src.llm_agents.llm_model import get_gemini_model
from src.llm_agents.prompt.chatbot_kg_distill_prompt import RETRIEVE_KG_SYSTEM_PROMPT, RETRIEVE_KG_HUMAN_PROMPT,  KG_FILTERED_SYSTEM_PROMPT, \
    KG_FILTERED_HUMAN_PROMPT
from src.llm_agents.prompt.chatbot_output_prompt import CHATBOT_OUTPUT_SYSTEM_PROMPT
from src.model.general_model import SocketEvent
from src.service.vector_db.vector_db_manager import VectorDBManager
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer
from src.utility.utility_method import parse_block


class ChatbotAgent(GraphAgent):

    def __init__(self, user_id: str, session_id: str, socket_id: str,
                 messages: List[ChatMessage], vector_db: VectorDBManager):
        self._user_id = user_id
        self._session_id = session_id
        self._socket_id = socket_id
        self._messages = messages
        self._vector_db = vector_db

    async def _retrieve_kg_graph(self, state: ChatbotAgentState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=JsonOutputParser(pydantic_object=KGRetrieveType),
            system_prompt_text=RETRIEVE_KG_SYSTEM_PROMPT,
            partial_variables={'summary': state['summary'], 'user_query': state['query']},
            human_prompt_text=RETRIEVE_KG_HUMAN_PROMPT,
        ).with_config({"run_name": 'Retrieve KG Graph'})

        r = await chain.ainvoke({})

        triples = convert_triple_list_to_pydantic(r['triples'])
        triples = await convert_triple_list_to_embedding(triples)

        retrieve_triples = await retrieve_relate_triples(session_id=self._session_id, kg_triples=triples, vector_db=self._vector_db)

        return {'kg_triples': triples, 'retrieve_triples': retrieve_triples}

    async def _merge_kg_graph(self, state: ChatbotAgentState):

        try:
            prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
            chain = prompt_factory.create_chain(
                output_parser=StrOutputParser(),
                system_prompt_text=KG_FILTERED_SYSTEM_PROMPT,
                human_prompt_text=KG_FILTERED_HUMAN_PROMPT,
                partial_variables={
                    'number': 10,
                    'retrieve_triples': convert_triple_list_to_string(state['retrieve_triples']),
                    'kg_triples': convert_triple_list_to_string(state['kg_triples'])
                }
            ).with_config({"run_name": 'Merge KG Graph'})

            r = await chain.ainvoke({})

            plan_json = json.loads(parse_block('json', r))

            return {'filtered_triples': convert_triple_list_to_pydantic(plan_json['triples']) }
        except Exception as e:
            return {'filtered_triples': []}

    async def _output_chat(self, state: ChatbotAgentState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        prompt_template = db_message_to_prompt(system_prompt=CHATBOT_OUTPUT_SYSTEM_PROMPT,
                                               human_prompt=state['query'],
                                               messages=self._messages)

        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            prompt_template=prompt_template,
            partial_variables={'long_term_plan': state['long_term_plan'],
                               'summary': state['summary'],
                               'triples': convert_triple_list_to_string(state['kg_triples'])}
        ).with_config({"run_name": 'Long term plan'})

        simple_streamer = SimplePromptStreamer(session_id=self._session_id, socket_id=self._socket_id, event_tag=SocketEvent.bot)

        print('Entering Output chat stream')
        result = await simple_streamer.execute(chain=chain)

        return {'output': result}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('init', lambda state: state)
        g_workflow.add_node('state_0_retrieve_kg', self._retrieve_kg_graph)
        g_workflow.add_node('state_2_merge_kg', self._merge_kg_graph)
        g_workflow.add_node('state_5_chat_output', self._output_chat)

        g_workflow.set_entry_point('init')
        g_workflow.add_edge('init', 'state_0_retrieve_kg')

        g_workflow.add_edge('state_0_retrieve_kg', 'state_2_merge_kg')
        g_workflow.add_edge('state_2_merge_kg', 'state_5_chat_output')
        g_workflow.add_edge('state_5_chat_output', END)

        g_compile = g_workflow.compile()

        return g_compile

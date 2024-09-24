import json

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.chatbot.chatbot_agent_type import ChatbotAgentState, KGRetrieveType, TripleType
from src.llm_agents.chatbot.chatbot_db import save_to_graph_db
from src.llm_agents.chatbot.chatbot_util import convert_triple_list_to_pydantic, convert_triple_list_to_string
from src.llm_agents.llm_model import get_gemini_model
from src.llm_agents.prompt.chatbot_kg_distill_prompt import RETRIVE_KG_SYSTEM_PROMPT
from src.llm_agents.prompt.chatbot_output_prompt import CHATBOT_OUTPUT_SYSTEM_PROMPT, CHATBOT_OUTPUT_HUMAN_PROMPT
from src.llm_agents.prompt.chatbot_plan_prompt import LONG_TERM_PLAN_HUMAN_PROMPT, LONG_TERM_PLAN_SYSTEM_PROMPT
from src.service.graph_db.neo4j_entry import get_async_neo4j_driver, triple_to_cypher
from src.service.graph_db.neo4j_static import MESSAGE_TRIPLE_TABLE
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer
from src.utility.utility_method import parse_block


class ChatbotAgent(GraphAgent):

    def __init__(self, user_id: str, session_id: str, chat_summary: str):
        self._user_id = user_id
        self._session_id = session_id
        self._chat_summary = str

    async def _retreive_kg_graph(self, state: ChatbotAgentState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=JsonOutputParser(pydantic_object=KGRetrieveType),
            system_prompt_text=RETRIVE_KG_SYSTEM_PROMPT,
            human_prompt_text=state['query']
        ).with_config({"run_name": 'Retrieve KG Graph'})

        r = await chain.ainvoke({})

        triples = convert_triple_list_to_pydantic(r['triples'])

        # await save_to_graph_db(
        #     user_id='hsinpa', session_id='session_01',
        #     chatbot_id='chatbot_01',
        #     triple_list=triples
        # )

        return {'kg_triples': triples}

    async def _long_term_plan(self, state: ChatbotAgentState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=LONG_TERM_PLAN_SYSTEM_PROMPT,
            human_prompt_text=LONG_TERM_PLAN_HUMAN_PROMPT,
            partial_variables={'long_term_plan': '', 'triples': convert_triple_list_to_string(state['kg_triples'])}
        ).with_config({"run_name": 'Long term plan'})

        r = await chain.ainvoke({})

        plan_json = json.loads(parse_block('json', r))

        strategy = plan_json['strategy']
        plans = convert_triple_list_to_string(convert_triple_list_to_pydantic(plan_json['plan']))

        plan_str = f'戰略: {strategy}\n\n採用短期策略:\n{plans}'

        return {'long_term_plan': plan_str}

    async def _output_chat(self, state: ChatbotAgentState):
        simple_streamer = SimplePromptStreamer(user_id=self._user_id, session_id=self._session_id)

        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=CHATBOT_OUTPUT_SYSTEM_PROMPT,
            human_prompt_text=CHATBOT_OUTPUT_HUMAN_PROMPT,
            partial_variables={'long_term_plan': state['long_term_plan'],
                               'query': state['query'],
                               'triples': convert_triple_list_to_string(state['kg_triples'])}
        ).with_config({"run_name": 'Output Chat'})

        result = await simple_streamer.execute(chain=chain)

        return {'output': result}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('state_0_retrieve_kg', self._retreive_kg_graph)
        g_workflow.add_node('state_4_long_term_plan', self._long_term_plan)
        g_workflow.add_node('state_5_chat_output', self._output_chat)

        g_workflow.set_entry_point('state_0_retrieve_kg')
        g_workflow.add_edge('state_0_retrieve_kg', 'state_4_long_term_plan')
        g_workflow.add_edge('state_4_long_term_plan', 'state_5_chat_output')
        g_workflow.add_edge('state_5_chat_output', END)

        g_compile = g_workflow.compile()

        return g_compile

from langchain_core.output_parsers import JsonOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.chatbot.chatbot_agent_type import ChatbotAgentState, KGRetrieveType, TripleType
from src.llm_agents.chatbot.chatbot_util import convert_triple_list_to_pydantic
from src.llm_agents.llm_model import get_gemini_model
from src.llm_agents.prompt.chatbot_kg_distill_prompt import RETRIVE_KG_SYSTEM_PROMPT
from src.service.graph_db.neo4j_entry import get_async_neo4j_driver, triple_to_cypher
from src.utility.simple_prompt_factory import SimplePromptFactory


class ChatbotAgent(GraphAgent):

    def __init__(self, user_id: str, session_id: str, chat_summary: str):
        self._user_id = user_id
        self._session_id = session_id
        self._chat_summary = str

    async def _retreive_kg_graph(self, state: ChatbotAgentState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model(), trace_name="Retrieve KG Graph")
        chain = prompt_factory.create_chain(
            output_parser=JsonOutputParser(pydantic_object=KGRetrieveType),
            system_prompt_text=RETRIVE_KG_SYSTEM_PROMPT,
            human_prompt_text=state['query']
        )

        r = await chain.ainvoke({})

        triples = convert_triple_list_to_pydantic(r['triples'])

        await self._save_to_graph_db(triple_list=triples)

        return {'kg_triples': triples}

    async def _save_to_graph_db(self, triple_list: list[TripleType]):
        neo4j_driver = get_async_neo4j_driver()

        async with neo4j_driver.session() as driver:
            for triple in triple_list:
                query, q_parameter = triple_to_cypher(triple_type=triple,
                                                      user_id='hsinpa', session_id='session_01',
                                                      chatbot_id='chatbot_01')

                await driver.run(query=query, parameters=q_parameter)

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('state_0_retrieve_kg', self._retreive_kg_graph)

        g_workflow.set_entry_point('state_0_retrieve_kg')
        g_workflow.add_edge('state_0_retrieve_kg', END)

        g_compile = g_workflow.compile()

        return g_compile

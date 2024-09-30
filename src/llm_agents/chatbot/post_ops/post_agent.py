import json
from typing import List

from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.llm_agents.chatbot.chatbot_agent_type import ChatbotPostState, ChatMessage
from src.llm_agents.chatbot.chatbot_util import convert_triple_list_to_string, db_message_to_prompt, \
    convert_triple_list_to_pydantic
from src.llm_agents.llm_model import get_gemini_model
from src.llm_agents.prompt.chatbot_kg_distill_prompt import KG_SUMMARY_SYSTEM_PROMPT, KG_SUMMARY_HUMAN_PROMPT, \
    KG_UPSERT_SYSTEM_PROMPT, KG_UPSERT_HUMAN_PROMPT
from src.llm_agents.prompt.chatbot_plan_prompt import LONG_TERM_PLAN_SYSTEM_PROMPT, LONG_TERM_PLAN_HUMAN_PROMPT
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.utility_method import parse_block


class PostAgent:
    def __init__(self, user_id: str, session_id: str, messages: List[ChatMessage]):
        self._user_id = user_id
        self._session_id = session_id
        self._messages = messages

    async def _update_summary(self, state: ChatbotPostState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=KG_SUMMARY_SYSTEM_PROMPT,
            human_prompt_text=KG_SUMMARY_HUMAN_PROMPT,
            partial_variables={'long_term_plan': state['long_term_plan'],
                               'summary': state['summary'],
                               'triples': convert_triple_list_to_string(state['kg_triples'])}
        ).with_config({"run_name": 'Summary'})

        r = await chain.ainvoke({})

        return {'summary': r}

    async def _update_kg_node(self, state: ChatbotPostState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=KG_UPSERT_SYSTEM_PROMPT,
            human_prompt_text=KG_UPSERT_HUMAN_PROMPT,
            partial_variables={'new_nodes': convert_triple_list_to_string(state['kg_triples'], with_id=True),
                               'previous_nodes': convert_triple_list_to_string(state['retrieve_triples'], with_id=True)}
        ).with_config({"run_name": 'Summary'})
        r = await chain.ainvoke({})

        plan_json = json.loads(parse_block('json', r))
        return {'delete_triples': plan_json['delete_nodes']}

    async def _long_term_plan(self, state: ChatbotPostState):
        try:
            prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())

            prompt_template = db_message_to_prompt(system_prompt=LONG_TERM_PLAN_SYSTEM_PROMPT,
                                                   human_prompt=LONG_TERM_PLAN_HUMAN_PROMPT,
                                                   messages=self._messages)

            chain = prompt_factory.create_chain(
                output_parser=StrOutputParser(),
                prompt_template=prompt_template,
                partial_variables={'long_term_plan': state['long_term_plan'],
                                   'summary': state['summary'],
                                   'db_triples': convert_triple_list_to_string(state['filtered_triples']),
                                   'input_triples': convert_triple_list_to_string(state['kg_triples'])}
            ).with_config({"run_name": 'Long term plan'})

            r = await chain.ainvoke({})

            plan_json = json.loads(parse_block('json', r))

            strategy = plan_json['strategy']
            plans = convert_triple_list_to_string(convert_triple_list_to_pydantic(plan_json['plan']))

            plan_str = f'戰略: {strategy}\n\n採用短期策略:\n{plans}'

            return {'long_term_plan': plan_str}

        except Exception as ex:
            print('ERROR long_term_plan')

    def create_graph(self):
        g_workflow = StateGraph(ChatbotPostState)

        g_workflow.add_node('init', lambda state: state)
        g_workflow.add_node('summary_node', self._update_summary)
        g_workflow.add_node('kg_node', self._update_kg_node)
        g_workflow.add_node('long_term_plan_node', self._long_term_plan)

        g_workflow.set_entry_point('init')
        g_workflow.add_edge('init', 'summary_node')
        g_workflow.add_edge('init', 'kg_node')
        g_workflow.add_edge('init', 'long_term_plan_node')

        g_workflow.add_edge(['summary_node', 'kg_node', 'long_term_plan_node'], END)

        return g_workflow.compile()

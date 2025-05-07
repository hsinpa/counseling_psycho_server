from langgraph.graph.graph import CompiledGraph
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.supervisor.homework.prompt.homework_3_2_3_en_prompt import  \
    HOMEWORK_3_2_3_ACTION_PLAN_PROMPT
from src.llm_agents.supervisor.homework.prompt.homework_3_2_4_en_prompt import HOMEWORK_3_2_4_ASSIGNMENT_PROMPT
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.static_text import OpenAI_Model_4o, Gemini_Model_2_0_Flash, OpenAI_Model_41_mini
from src.utility.utility_method import parse_json
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.llm_model import ILLMLoader
from src.llm_agents.supervisor.homework.homework_state import HomeworkState

class HomeworkGraph(GraphAgent):

    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    async def _action_plan_node(self, state: HomeworkState):
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=HOMEWORK_3_2_3_ACTION_PLAN_PROMPT,
        ).with_config({"run_name": 'Homework: 3-2-3 Action plan'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'therapy_issue_and_objective': state['therapy_issue_objective'],
                                 })
        return {'action_plan': r}

    async def _homework_assignment_node(self, state: HomeworkState):
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=HOMEWORK_3_2_4_ASSIGNMENT_PROMPT,
        ).with_config({"run_name": 'Homework: 3-2-4 Assignment'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'action_plan': state['action_plan'],
                                 'knowledge_graph_issue': state['knowledge_graph_issue'],
                                 })
        return {'homework_assignment': r}

    def create_graph(self) -> CompiledGraph:
        g_workflow = StateGraph(HomeworkState)

        g_workflow.add_node('start_node', lambda x: x)
        g_workflow.add_node('action_plan_node', self._action_plan_node)
        g_workflow.add_node('homework_assignment_node', self._homework_assignment_node)

        g_workflow.set_entry_point('start_node')
        g_workflow.add_edge('start_node', 'action_plan_node')
        g_workflow.add_edge('action_plan_node', 'homework_assignment_node')
        g_workflow.add_edge('homework_assignment_node', END)

        return g_workflow.compile()
from langgraph.graph.graph import CompiledGraph
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.llm_model import ILLMLoader
from src.llm_agents.supervisor.case_concept.case_concept_state import CaseConceptState
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_1_en_prompt import \
    PREREQUISITE_PROMPT_1_1_TREATMENT_FRAMEWORK
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_2_en_prompt import \
    PREREQUISITE_PROMPT_1_2_THERAPY_OBJECTIVE
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.static_text import OpenAI_Model_41_mini


class CaseConceptGraph(GraphAgent):
    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    async def _treatment_framework_node(self, state: CaseConceptState):
        """Step 1_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(OpenAI_Model_41_mini))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_1_TREATMENT_FRAMEWORK,
        ).with_config({"run_name": '1-1 Treatment Framework'})

        r = await chain.ainvoke({'conversation': state['transcribe_text']})

        return {'treatment_framework': r}

    async def _therapy_issue_objective_node(self, state: CaseConceptState):
        """Step 1_2"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(OpenAI_Model_41_mini))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_2_THERAPY_OBJECTIVE,
        ).with_config({"run_name": '1-2 Therapy issue and Objective'})

        r = await chain.ainvoke({'conversation': state['transcribe_text']})

        return {'therapy_issue_objective': r}

    def create_graph(self) -> CompiledGraph:
        g_workflow = StateGraph(CaseConceptState)

        g_workflow.add_node('start_node', lambda x: x)
        g_workflow.add_node('treatment_framework_node', self._treatment_framework_node)
        g_workflow.add_node('therapy_issue_objective_node', self._therapy_issue_objective_node)
        g_workflow.add_node('merge_node', lambda state: state)

        g_workflow.set_entry_point('start_node')

        g_workflow.add_edge('start_node', 'treatment_framework_node')
        g_workflow.add_edge('start_node', 'therapy_issue_objective_node')

        g_workflow.add_edge(['treatment_framework_node', 'therapy_issue_objective_node'], 'merge_node')

        g_workflow.add_edge('merge_node', END)

        g_compile = g_workflow.compile()

        return g_compile
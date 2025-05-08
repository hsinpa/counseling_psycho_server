from langgraph.graph.graph import CompiledGraph
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.llm_model import ILLMLoader
from src.llm_agents.supervisor.case_treatment.case_treatment_state import CaseTreatmentState
from src.llm_agents.supervisor.case_treatment.prompt.case_treatment_3_2_0_en_prompt import \
    CASE_TREATMENT_PROMPT_3_2_0_INFORMATION
from src.llm_agents.supervisor.case_treatment.prompt.case_treatment_3_2_1_en_prompt import \
    CASE_TREATMENT_PROMPT_3_2_1_STRATEGY
from src.llm_agents.supervisor.case_treatment.prompt.case_treatment_3_2_2_en_prompt import \
    CASE_TREATMENT_PROMPT_3_2_2_EVALUATION
from src.llm_agents.supervisor.case_treatment.prompt.case_treatment_data import (
    Symptoms,
    Intervention_Techniques,
    THERAPEUTIC_HIERARCHY,
    Methods,
)
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.static_text import Gemini_Model_2_0_Flash


class CaseTreatmentGraph(GraphAgent):
    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    async def _case_treatment_info_node(self, state: CaseTreatmentState):
        """Step 3_2_0"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=CASE_TREATMENT_PROMPT_3_2_0_INFORMATION,
        ).with_config({"run_name": '3_2_0 Case Treatment Information '})

        r = await chain.ainvoke(
            {
                "therapy_issue_and_objective": state["therapy_issue_objective"],
                "treatment_framework": state["treatment_framework"],
                "knowledge_graph_of_issue": state["knowledge_graph_issue"],
                "symptoms": Symptoms,
                "intervention_techniques": Intervention_Techniques,
            },
        )

        return {'case_treatment_information': r}

    async def _case_treatment_strategy_node(self, state: CaseTreatmentState):
        """Step 3_2_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=CASE_TREATMENT_PROMPT_3_2_1_STRATEGY,
        ).with_config({"run_name": '3-2-1 Case treatment strategy'})

        r = await chain.ainvoke(
            {
                "case_treatment_information": state["case_treatment_information"],
                "method": Methods,
                "therapeutic_hierarchy": THERAPEUTIC_HIERARCHY,
            }
        )

        return {'case_treatment_strategy': r}

    async def _case_criteria_evaluation_node(self, state: CaseTreatmentState):
        """Step 3_2_2"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=CASE_TREATMENT_PROMPT_3_2_2_EVALUATION,
        ).with_config({"run_name": '3-2-1 Case treatment strategy'})

        r = await chain.ainvoke(
            {
                "case_treatment_information": state["case_treatment_information"],
                "case_treatment_strategy": state['case_treatment_strategy'],
            }
        )

        return {'case_phase_evaluation_criteria': r}

    def create_graph(self) -> CompiledGraph:
        g_workflow = StateGraph(CaseTreatmentState)

        g_workflow.add_node('case_treatment_info_node', self._case_treatment_info_node)
        g_workflow.add_node('case_treatment_strategy_node', self._case_treatment_strategy_node)
        g_workflow.add_node('case_criteria_evaluation_node', self._case_criteria_evaluation_node)

        g_workflow.set_entry_point('case_treatment_info_node')

        g_workflow.add_edge('case_treatment_info_node', 'case_treatment_strategy_node')
        g_workflow.add_edge('case_treatment_strategy_node', 'case_criteria_evaluation_node')

        g_workflow.add_edge('case_criteria_evaluation_node', END)

        g_compile = g_workflow.compile()

        return g_compile

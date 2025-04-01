from langgraph.graph.graph import CompiledGraph
from langgraph.constants import END
from langgraph.graph import StateGraph
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.llm_model import ILLMLoader
from src.llm_agents.supervisor.prerequisite.prerequisite_state import PrerequisiteState
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_1_en_prompt import \
    PREREQUISITE_PROMPT_1_1_TREATMENT_FRAMEWORK
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_2_en_prompt import \
    PREREQUISITE_PROMPT_1_2_THERAPY_OBJECTIVE
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_3_en_prompt import PREREQUISITE_PROMPT_1_3_METHOD_TECH
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_4_en_prompt import \
    PREREQUISITE_PROMPT_1_4_TREATMENT_PROGRESS
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_5_en_prompt import \
    PREREQUISITE_PROMPT_1_5_THERAPY_OUTCOME
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_1_6_en_prompt import \
    PREREQUISITE_PROMPT_1_6_TREATMENT_EFFECTIVENESS
from src.llm_agents.supervisor.prerequisite.prompt.prerequisite_3_1_en_prompt import \
    PREREQUISITE_PROMPT_3_1_THERAPY_DIRECTION
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.static_text import OpenAI_Model_4o, Gemini_Model_2_0_Flash
from src.utility.utility_method import parse_json


class PrerequisiteGraph(GraphAgent):
    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    async def _treatment_framework_node(self, state: PrerequisiteState):
        """Step 1_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(OpenAI_Model_4o))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_1_TREATMENT_FRAMEWORK,
        ).with_config({"run_name": '1-1 Treatment Framework'})

        r = await chain.ainvoke({'conversation': state['transcribe_text']})

        return {'treatment_framework': r}

    async def _therapy_issue_objective_node(self, state: PrerequisiteState):
        """Step 1_2"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(OpenAI_Model_4o))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_2_THERAPY_OBJECTIVE,
        ).with_config({"run_name": '1-2 Therapy issue and Objective'})

        r = await chain.ainvoke({'conversation': state['transcribe_text']})

        return {'therapy_issue_objective': r}

    async def _method_technique_node(self, state: PrerequisiteState):
        """Step 1_3"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_3_METHOD_TECH,
        ).with_config({"run_name": '1-3 Method technique'})

        r = await chain.ainvoke({'conversation': state['transcribe_text']})

        return {'methods_and_techniques': r}

    async def _treatment_progress_node(self, state: PrerequisiteState):
        """Step 1_4"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_4_TREATMENT_PROGRESS,
        ).with_config({"run_name": '1-4 Treatment Progress'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'therapy_issue_and_objective': state['therapy_issue_objective'],
                                'treatment_framework': state['treatment_framework']})

        return {'treatment_progress': r}

    async def _therapy_outcome_node(self, state: PrerequisiteState):
        """Step 1_5"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_5_THERAPY_OUTCOME,
        ).with_config({"run_name": '1-5 Therapy outcome'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'therapy_issue_and_objective': state['therapy_issue_objective'],
                                 'methods_and_techniques': state['methods_and_techniques']
                                 })

        return {'therapy_outcome': r}

    async def _treatment_effectiveness_node(self, state: PrerequisiteState):
        """Step 1_6"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_1_6_TREATMENT_EFFECTIVENESS,
        ).with_config({"run_name": '1-6 Treatment Effectiveness'})

        r = await chain.ainvoke({'progress': state['treatment_progress'],
                                 'therapy_outcome': state['therapy_outcome']})

        return {'treatment_effectiveness': r}

    async def _therapy_direction_node(self, state: PrerequisiteState):
        """Step 3_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=PREREQUISITE_PROMPT_3_1_THERAPY_DIRECTION,
        ).with_config({"run_name": '3-1 Therapy Direction'})

        r = await chain.ainvoke({'progress': state['treatment_progress'],
                                 'treatment_effectiveness': state['treatment_effectiveness']})
        r_json = parse_json(r)
        return {'next_session_therapy_direction': r_json['next_session_therapy_direction'],
                'short_to_mid_term_therapy_direction': r_json['short_to_mid_term_therapy_direction'],
                'long_term_therapy_direction': r_json['long_term_therapy_direction']}

    def create_graph(self) -> CompiledGraph:
        g_workflow = StateGraph(PrerequisiteState)

        g_workflow.add_node('start_node', lambda x: x)
        g_workflow.add_node('treatment_framework_node', self._treatment_framework_node)
        g_workflow.add_node('therapy_issue_objective_node', self._therapy_issue_objective_node)
        g_workflow.add_node('method_technique_node', self._method_technique_node)

        g_workflow.add_node('treatment_progress_node', self._treatment_progress_node)
        g_workflow.add_node('therapy_outcome_node', self._therapy_outcome_node)

        g_workflow.add_node('treatment_effectiveness_node', self._treatment_effectiveness_node)
        g_workflow.add_node('therapy_direction_node', self._therapy_direction_node)

        g_workflow.set_entry_point('start_node')

        g_workflow.add_edge('start_node', 'treatment_framework_node')
        g_workflow.add_edge('start_node', 'therapy_issue_objective_node')
        g_workflow.add_edge('start_node', 'method_technique_node')

        g_workflow.add_edge(['treatment_framework_node', 'therapy_issue_objective_node'], 'treatment_progress_node')
        g_workflow.add_edge(['method_technique_node', 'therapy_issue_objective_node'], 'therapy_outcome_node')

        g_workflow.add_edge(['treatment_progress_node', 'therapy_outcome_node'], 'treatment_effectiveness_node')

        g_workflow.add_edge(['treatment_progress_node', 'treatment_effectiveness_node'], 'therapy_direction_node')

        g_workflow.add_edge('therapy_direction_node', END)

        g_compile = g_workflow.compile()

        return g_compile
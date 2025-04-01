from langgraph.graph.graph import CompiledGraph
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from src.llm_agents.agent_interface import GraphAgent
from src.llm_agents.llm_model import ILLMLoader
from src.llm_agents.supervisor.strategy.prompt.strategy_2_1_en_prompt import STRATEGY_PROMPT_2_1_COGNITIVE_MODEL
from src.llm_agents.supervisor.strategy.prompt.strategy_2_2_1_en_prompt import STRATEGY_PROMPT_2_2_1_MEAN_OF_AT
from src.llm_agents.supervisor.strategy.prompt.strategy_2_2_en_prompt import \
    STRATEGY_PROMPT_2_2_CORE_INTERMEDIATE_BELIEF
from src.llm_agents.supervisor.strategy.prompt.strategy_2_3_1_en_prompt import \
    STRATEGY_PROMPT_2_2_1_RELEVANT_HISTORY_PRECIPITANTS
from src.llm_agents.supervisor.strategy.prompt.strategy_2_3_2_en_prompt import STRATEGY_PROMPT_2_3_2_COPING_STRATEGY
from src.llm_agents.supervisor.strategy.strategy_state import StrategyState
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.static_text import OpenAI_Model_4o, Gemini_Model_2_0_Flash
from src.utility.utility_method import parse_json
from langchain_core.output_parsers import StrOutputParser


class StrategyGraph(GraphAgent):

    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    async def _cognitive_model_node(self, state: StrategyState):
        """Step 2_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(OpenAI_Model_4o))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_1_COGNITIVE_MODEL,
        ).with_config({"run_name": '2-1 COGNITIVE MODEL'})

        r = await chain.ainvoke({'conversation': state['transcribe_text']})

        return {'cognitive_model': r}

    async def _core_intermediate_belief_node(self, state: StrategyState):
        """Step 2_2"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_2_CORE_INTERMEDIATE_BELIEF,
        ).with_config({"run_name": '2-1 Core intermediate belief'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'], 'cognitive_model': state['cognitive_model']})

        return {'core_intermediate_belief': r}

    async def _mean_of_at_node(self, state: StrategyState):
        """Step 2_2_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_2_1_MEAN_OF_AT,
        ).with_config({"run_name": '2-1-1 MEAN OF AT'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'core_belief_and_intermediate_belief': state['core_intermediate_belief']})

        return {'core_intermediate_belief': r}

    async def _relevant_history_precipitants_node(self, state: StrategyState):
        """Step 2_3_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_2_1_RELEVANT_HISTORY_PRECIPITANTS,
        ).with_config({"run_name": '2-3-1 Relevant History Precipitants'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'cognitive_model': state['cognitive_model'],
                                 'core_belief_and_intermediate_belief': state['core_intermediate_belief']})

        return {'relevant_history_precipitants': r}


    async def _coping_strategy_node(self, state: StrategyState):
        """Step 2_3_2"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_3_2_COPING_STRATEGY,
        ).with_config({"run_name": '2-3-1 Relevant History Precipitants'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'cognitive_model': state['cognitive_model'],
                                 'relevant_history_and_precipitants': state['relevant_history_precipitants'],
                                 'core_belief_and_intermediate_belief': state['core_intermediate_belief']})

        return {'coping_strategy': r}

    def create_graph(self) -> CompiledGraph:
        g_workflow = StateGraph(StrategyState)

        g_workflow.add_node('cognitive_model_node', self._cognitive_model_node)
        g_workflow.add_node('core_intermediate_belief_node', self._core_intermediate_belief_node)
        g_workflow.add_node('relevant_history_precipitants_node', self._relevant_history_precipitants_node)
        g_workflow.add_node('copy_strategy_node', self._coping_strategy_node)

        g_workflow.add_edge(START, 'cognitive_model_node')
        g_workflow.add_edge('cognitive_model_node', 'core_intermediate_belief_node')
        g_workflow.add_edge('core_intermediate_belief_node', 'relevant_history_precipitants_node')
        g_workflow.add_edge('relevant_history_precipitants_node', 'copy_strategy_node')
        g_workflow.add_edge('copy_strategy_node', END)

        return g_workflow.compiled()


import asyncio
from langgraph.graph.graph import CompiledGraph
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from src.feature.agent_interface import GraphAgent
from src.feature.llm_model import ILLMLoader
from src.feature.supervisor.strategy.prompt.strategy_2_1_1_en_prompt import STRATEGY_PROMPT_2_1_1_SITUATIONS
from src.feature.supervisor.strategy.prompt.strategy_2_1_en_prompt import STRATEGY_PROMPT_2_1_COGNITIVE_MODEL
from src.feature.supervisor.strategy.prompt.strategy_2_2_1_en_prompt import STRATEGY_PROMPT_2_2_1_MEAN_OF_AT
from src.feature.supervisor.strategy.prompt.strategy_2_2_en_prompt import \
    STRATEGY_PROMPT_2_2_CORE_INTERMEDIATE_BELIEF
from src.feature.supervisor.strategy.prompt.strategy_2_3_1_en_prompt import \
    STRATEGY_PROMPT_2_2_1_RELEVANT_HISTORY_PRECIPITANTS
from src.feature.supervisor.strategy.prompt.strategy_2_3_2_en_prompt import STRATEGY_PROMPT_2_3_2_COPING_STRATEGY
from src.feature.supervisor.strategy.prompt.strategy_2_3_3_en_prompt import \
    STRATEGY_PROMPT_2_3_3_SITUATION_RELEVANT_ISSUE
from src.feature.supervisor.strategy.prompt.strategy_2_3_4_en_prompt import \
    STRATEGY_PROMPT_2_3_4_KNOWLEDGE_GRAPH_ISSUE
from src.feature.supervisor.strategy.prompt.strategy_3_2_1_en_prompt import STRATEGY_PROMPT_3_2_1_NEXT_THERAPY_GOAL
from src.feature.supervisor.strategy.prompt.strategy_3_2_2_en_prompt import STRATEGY_PROMPT_3_2_2_TREATMENT_STRATEGY
from src.feature.supervisor.strategy.strategy_state import StrategyState
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.static_text import Gemini_Model_2_0_Flash, OpenAI_Model_41_mini
from src.utility.utility_method import parse_json
from langchain_core.output_parsers import StrOutputParser


class StrategyGraph(GraphAgent):

    def __init__(self, llm_loader: ILLMLoader):
        self._llm_loader = llm_loader

    async def _client_situations_node(self, state: StrategyState):
        """Step 2_1_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_1_1_SITUATIONS,
        ).with_config({"run_name": '2-1-1 CLIENT SITUATIONS'})

        r = await chain.ainvoke({'conversation': state['transcribe_text']})

        return {'client_situations': r}

    async def _cognitive_model_node(self, state: StrategyState):
        """Step 2_1"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_1_COGNITIVE_MODEL,
        ).with_config({"run_name": '2-1 COGNITIVE MODEL'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'], 'client_situations': state['client_situations']})

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
        ).with_config({"run_name": '2-1-1 MEANING OF AT'})

        r = await chain.ainvoke({'cognitive_model': state['cognitive_model'],
                                 'core_belief_and_intermediate_belief': state['core_intermediate_belief']})

        return {'meaning_of_AT': r}

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
        ).with_config({"run_name": '2-3-2 Coping Strategy'})

        r = await chain.ainvoke({'conversation': state['transcribe_text'],
                                 'cognitive_model': state['cognitive_model'],
                                 'relevant_history_and_precipitants': state['relevant_history_precipitants'],
                                 'core_belief_and_intermediate_belief': state['core_intermediate_belief']})

        return {'coping_strategies': r}

    async def _situation_relevant_issue_node(self, state: StrategyState):
        """Step 2_3_3"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(OpenAI_Model_41_mini))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_3_3_SITUATION_RELEVANT_ISSUE,
        ).with_config({"run_name": '2-3-3 Situation Relevant Issue'})

        r = await chain.ainvoke({'cognitive_model': state['cognitive_model'],
                                 'therapy_issue_and_objective': state['therapy_issue_objective']})
        return {'situations_relevant_to_issue': r}

    async def _batch_knowledge_graph_issue_node(self, state: StrategyState):
        therapeutic_issues: list = parse_json(state['therapy_issue_objective'])['therapeutic_issues']
        results = []

        async with asyncio.TaskGroup() as tg:
            # Store task references if you need results
            tasks = [tg.create_task(self._knowledge_graph_issue_node(state, i)) for i in therapeutic_issues]

        for task in tasks:
            results.append(task.result())

        return {'knowledge_graph_issue': '\n'.join(results)}

    async def _knowledge_graph_issue_node(self, state: StrategyState, issue: dict):
        """Step 2_3_4"""
        prompt_factory = SimplePromptFactory(llm_model=self._llm_loader.get_llm_model(Gemini_Model_2_0_Flash))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=STRATEGY_PROMPT_2_3_4_KNOWLEDGE_GRAPH_ISSUE,
        ).with_config({"run_name": '2-3-4 Batch Knowledge Graph'})

        r = await chain.ainvoke({'coping_strategy': state['coping_strategies'],
                                 'therapy_issue_and_objective': state['therapy_issue_objective'],
                                 'chosen_issue': issue,
                                 'cognitive_model': state['cognitive_model'],
                                 'situations_relevant_to_issue': state['situations_relevant_to_issue'],
                                 'relevant_history_and_precipitants': state['relevant_history_precipitants'],
                                 'core_belief_and_intermediate_belief': state['core_intermediate_belief']})

        return r

    def create_graph(self) -> CompiledGraph:
        g_workflow = StateGraph(StrategyState)

        g_workflow.add_node('client_situations_node', self._client_situations_node)
        g_workflow.add_node('cognitive_model_node', self._cognitive_model_node)
        g_workflow.add_node('core_intermediate_belief_node', self._core_intermediate_belief_node)
        g_workflow.add_node('relevant_history_precipitants_node', self._relevant_history_precipitants_node)
        g_workflow.add_node('copy_strategy_node', self._coping_strategy_node)
        g_workflow.add_node('mean_of_at_node', self._mean_of_at_node)
        g_workflow.add_node('situation_relevant_issue_node', self._situation_relevant_issue_node)
        g_workflow.add_node('knowledge_graph_issue_node', self._batch_knowledge_graph_issue_node)

        g_workflow.add_node('final_merge_node', lambda state: state)

        g_workflow.add_edge(START, 'client_situations_node')
        g_workflow.add_edge('client_situations_node', 'cognitive_model_node')
        g_workflow.add_edge('cognitive_model_node', 'core_intermediate_belief_node')
        g_workflow.add_edge('cognitive_model_node', 'situation_relevant_issue_node')

        g_workflow.add_edge('core_intermediate_belief_node', 'mean_of_at_node')
        g_workflow.add_edge('core_intermediate_belief_node', 'relevant_history_precipitants_node')
        g_workflow.add_edge(['relevant_history_precipitants_node', 'mean_of_at_node'], 'copy_strategy_node')

        g_workflow.add_edge(['copy_strategy_node', 'situation_relevant_issue_node'], 'knowledge_graph_issue_node')

        g_workflow.add_edge('knowledge_graph_issue_node', 'final_merge_node')
        g_workflow.add_edge('final_merge_node', END)

        return g_workflow.compile()

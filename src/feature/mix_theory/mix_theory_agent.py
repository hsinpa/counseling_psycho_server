import asyncio

from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END, START
from langgraph.graph import StateGraph

from src.feature.llm_model import get_gpt_model
from src.feature.mix_theory.mix_theory_prompt_analysis import MIX_THEORY_ANALYSIS_HUMAN_PROMPT
from src.feature.mix_theory.mix_theory_prompt_question import MIX_THEORY_QUESTION_HUMAN_PROMPT
from src.feature.mix_theory.mix_theory_prompt_strategy import MIX_THEORY_STRATEGY_HUMAN_PROMPT
from src.feature.mix_theory.mix_theory_type import MixTheoryGraphState
from src.feature.share_component.theory_components import select_theory_chain
from src.model.general_model import SocketEvent
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer
from src.utility.theory_utility import psycho_theory_to_text, GLOBAL_PSYCHO_THEORY_TEXT


class MixTheoryAgent:

    def __init__(self, socket_id: str, token_ids: list[str]):
        self._socket_id = socket_id
        self._token_ids = token_ids

    def _theory_condition_branch(self, state: MixTheoryGraphState):
        if len(state['selected_theory_list']) > 0:
            return 'output_reports'
        else:
            return 'select_theories'

    async def _select_theory_chain(self, state: MixTheoryGraphState):
        selected_questionnaire_list = await select_theory_chain(
            basic_info=state['user_info'],
            questionnaire_full_text=GLOBAL_PSYCHO_THEORY_TEXT
        )

        return {'selected_theory_list': selected_questionnaire_list}

    async def _output_reports_chain(self, state: MixTheoryGraphState):
        theories_text = psycho_theory_to_text(state['selected_theory_list'])
        async with asyncio.TaskGroup() as tg:
            analysis_task = tg.create_task(self._generic_report_chain(name='analysis_report', token=self._token_ids[0], basic_info=state['user_info'],
                                                              theories_text=theories_text,
                                                              human_prompt=MIX_THEORY_ANALYSIS_HUMAN_PROMPT))

            question_task = tg.create_task(self._generic_report_chain(name='question_report', token=self._token_ids[1], basic_info=state['user_info'],
                                                              theories_text=theories_text,
                                                              human_prompt=MIX_THEORY_QUESTION_HUMAN_PROMPT))

            strategy_task = tg.create_task(self._generic_report_chain(name='strategy_report', token=self._token_ids[2], basic_info=state['user_info'],
                                                              theories_text=theories_text,
                                                              human_prompt=MIX_THEORY_STRATEGY_HUMAN_PROMPT))


        return {'analysis_report' : analysis_task.result(), 'question_report': question_task.result(), 'strategy_report': strategy_task.result()}

    async def _generic_report_chain(self, name: str, token: str, basic_info: str, theories_text, human_prompt: str):
        prompt_factory = SimplePromptFactory(llm_model=get_gpt_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=human_prompt,
            partial_variables={
                'basic_info': basic_info,
                'theories': theories_text
            }
        ).with_config({"run_name": name})

        simple_streamer = SimplePromptStreamer(session_id=token, socket_id=self._socket_id, event_tag=SocketEvent.bot)
        result = await simple_streamer.execute(chain=chain)

        print(name, result)
        return result

    def compile_graph(self):
        g_workflow = StateGraph(MixTheoryGraphState)

        g_workflow.add_node('select_theories', self._select_theory_chain)
        g_workflow.add_node('output_reports', self._output_reports_chain)

        g_workflow.add_conditional_edges(
            source=START,
            path=self._theory_condition_branch,
            # path_map={"output_reports": "output_reports", "select_theories": "select_theories"},
        )
        g_workflow.add_edge('select_theories', 'output_reports')
        g_workflow.add_edge('output_reports', END)

        g_compile = g_workflow.compile()

        return g_compile


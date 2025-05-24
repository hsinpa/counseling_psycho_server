import json

from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from src.feature.llm_model import get_gemini_model
from src.feature.share_component.theory_components import select_theory_chain
from src.feature.talk_simulation.detail_report.report_theory_prompt import PICK_THEORY_SYSTEM_PROMPT, \
    PICK_THEORY_HUMAN_PROMPT, ACCURATE_REPORT_SYSTEM_PROMPT, ACCURATE_REPORT_HUMAN_PROMPT
from src.feature.talk_simulation.detail_report.report_theory_type import ReportTheoryGraphState
from src.feature.talk_simulation.talk_simulation_helper import basic_info_to_string, questionaries_to_string
from src.model.general_model import SocketEvent
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.tests.talk_simulation.test_gen_answer import user_info
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer
from src.utility.theory_utility import GLOBAL_PSYCHO_THEORY_ARRAY, GLOBAL_PSYCHO_THEORY_TEXT, psycho_theory_to_text
from src.utility.utility_method import parse_block


class ReportTheoryAgent:
    def __init__(self, user_input: SimulationQuesUserInputType, socket_id: str):
        self._user_input = user_input
        self._socket_id = socket_id

    async def _select_theory_chain(self, state: ReportTheoryGraphState):
        selected_questionnaire_list = await select_theory_chain(
            basic_info=basic_info_to_string(self._user_input),
            questionnaire_full_text=state['questionnaire_full_text']
        )

        return {'selected_questionnaire_list': selected_questionnaire_list}

    async def _output_report_chain(self, state: ReportTheoryGraphState):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=ACCURATE_REPORT_SYSTEM_PROMPT,
            human_prompt_text=ACCURATE_REPORT_HUMAN_PROMPT,
            partial_variables={
                'basic_info': basic_info_to_string(self._user_input),
                'theories': psycho_theory_to_text(state['selected_questionnaire_list']),
                'questionnaire': state['questionnaire_full_text']
            }
        ).with_config({"run_name": 'Output Report'})

        simple_streamer = SimplePromptStreamer(session_id=self._user_input.session_id,
                                               socket_id=self._socket_id,
                                               event_tag=SocketEvent.bot)

        print('Entering Output report stream')
        result = await simple_streamer.execute(chain=chain)

        return {'report': result}

    async def compile_graph(self):
        g_workflow = StateGraph(ReportTheoryGraphState)

        g_workflow.add_node('select_theories', self._select_theory_chain)
        g_workflow.add_node('output_report', self._output_report_chain)

        g_workflow.set_entry_point('select_theories')
        g_workflow.add_edge('select_theories', 'output_report')
        g_workflow.add_edge('output_report', END)

        g_compile = g_workflow.compile()

        return g_compile


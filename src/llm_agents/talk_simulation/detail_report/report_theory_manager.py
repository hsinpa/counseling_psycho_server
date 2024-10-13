from typing import List

from pydantic import TypeAdapter
from langfuse.callback import CallbackHandler

from src.llm_agents.talk_simulation.detail_report.report_theory_agent import ReportTheoryAgent
from src.llm_agents.talk_simulation.detail_report.report_theory_type import ReportTheoryGraphState
from src.llm_agents.talk_simulation.talk_simulation_db_ops import db_ops_get_simulation_info, db_ops_save_output_report
from src.llm_agents.talk_simulation.talk_simulation_helper import questionaries_to_string
from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType, SimulationReportInput


class ReportTheoryManager:
    def __init__(self, user_input: SimulationReportInput):
        self._user_input = user_input

    async def execute_questionnaire_pipeline(self):
        user_info_json = db_ops_get_simulation_info(self._user_input.session_id)
        print(user_info_json)
        user_info: SimulationQuesUserInputType = SimulationQuesUserInputType(**user_info_json)

        # question_list_adapter = TypeAdapter(List[QuestionType])
        # question_list = question_list_adapter.validate_python(user_info_json['questionnaires'])

        agent = ReportTheoryAgent(user_info, self._user_input.socket_id)
        questions_graph = await agent.compile_graph()

        r: ReportTheoryGraphState = await questions_graph.ainvoke({
            'questionnaire_full_text': questionaries_to_string(self._user_input.questionnaires)
        }, {"run_name": 'Output accurate theory report', "callbacks": [CallbackHandler(user_id='hsinpa')] })

        db_ops_save_output_report(self._user_input.session_id, r['report'])

        return r
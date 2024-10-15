from typing import List

from pydantic import TypeAdapter
from langfuse.callback import CallbackHandler

from src.llm_agents.talk_simulation.detail_report.report_theory_agent import ReportTheoryAgent
from src.llm_agents.talk_simulation.detail_report.report_theory_type import ReportTheoryGraphState
from src.llm_agents.talk_simulation.talk_simulation_db_ops import db_ops_get_simulation_info, db_ops_save_output_report
from src.llm_agents.talk_simulation.talk_simulation_helper import questionaries_to_string, \
    questionnaire_records_to_string
from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType, StreamSimulationInput
from src.service.relation_db.sql_client_interface import SQLClientInterface


class ReportTheoryManager:
    def __init__(self, client: SQLClientInterface, user_input: StreamSimulationInput):
        self._user_input = user_input
        self._sql_client = client

    async def execute_report_pipeline(self):
        user_info_json = db_ops_get_simulation_info(self._sql_client, self._user_input.session_id)
        user_info: SimulationQuesUserInputType = SimulationQuesUserInputType(**user_info_json)

        question_list_adapter = TypeAdapter(List[List[QuestionType]])
        question_list = question_list_adapter.validate_python(user_info_json['questionnaires'])

        if user_info_json['report_flag'] is False:
            return user_info_json['report']

        agent = ReportTheoryAgent(user_info, self._user_input.socket_id)
        questions_graph = await agent.compile_graph()

        r: ReportTheoryGraphState = await questions_graph.ainvoke({
            'questionnaire_full_text': questionnaire_records_to_string(question_list)
        }, {"run_name": 'Output accurate theory report', "callbacks": [CallbackHandler(user_id='hsinpa')] })

        db_ops_save_output_report(self._user_input.session_id, r['report'])

        return r
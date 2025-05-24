import json
from typing import List

from pydantic import TypeAdapter

from src.feature.talk_simulation.answers.answer_question_agent import AnswerQuestionAgent
from src.feature.talk_simulation.talk_simulation_db_ops import db_ops_get_simulation_info
from src.feature.talk_simulation.talk_simulation_type import QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.service.relation_db.sql_client_interface import SQLClientInterface


class AnswerQuestionManager:
    def __init__(self, client: SQLClientInterface, session_id):
        self._session_id = session_id
        self._sql_client = client

    async def execute_questionnaire_pipeline(self):
        basic_info = db_ops_get_simulation_info(self._sql_client, self._session_id)
        user_input: SimulationQuesUserInputType = SimulationQuesUserInputType(**basic_info)

        # Rephrase questionnaire
        questionnaire_len = len(basic_info['questionnaires'])
        questionnaires_json = basic_info['questionnaires'][questionnaire_len - 1]

        question_list_adapter = TypeAdapter(List[QuestionType])
        question_list = question_list_adapter.validate_python(questionnaires_json)

        print(user_input.model_dump_json())
        print(json.dumps(questionnaires_json, ensure_ascii=False))

    
        agent = AnswerQuestionAgent(user_input, question_list)
        questions = await agent.execute_pipeline()

        return questions
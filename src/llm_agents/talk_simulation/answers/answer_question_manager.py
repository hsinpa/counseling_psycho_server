from typing import List

from pydantic import TypeAdapter

from src.llm_agents.talk_simulation.answers.answer_question_agent import AnswerQuestionAgent
from src.llm_agents.talk_simulation.talk_simulation_db_ops import db_ops_get_simulation_info
from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType


class AnswerQuestionManager:
    def __init__(self, session_id):
        self._session_id = session_id

    async def execute_questionnaire_pipeline(self):
        basic_info = db_ops_get_simulation_info(self._session_id)
        user_input: SimulationQuesUserInputType = SimulationQuesUserInputType(**basic_info)

        question_list_adapter = TypeAdapter(List[QuestionType])
        question_list = question_list_adapter.validate_python(basic_info['questionnaires'])

        agent = AnswerQuestionAgent(user_input, question_list)
        questions = await agent.execute_pipeline()

        return questions
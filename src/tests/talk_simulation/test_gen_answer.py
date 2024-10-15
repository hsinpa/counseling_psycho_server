from typing import List

import pytest
from pydantic import TypeAdapter

from src.llm_agents.talk_simulation.answers.answer_question_agent import AnswerQuestionAgent
from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.tests.dataset.questionnaires import Slot_Advanced_Questionnaire_With_No_Answer
from src.tests.dataset.user_info import Basic_User_Info


@pytest.fixture
def user_info():
    return SimulationQuesUserInputType(**Basic_User_Info)

@pytest.fixture
def questionnaires():
    question_list_adapter = TypeAdapter(List[QuestionType])
    question_list = question_list_adapter.validate_python(Slot_Advanced_Questionnaire_With_No_Answer)

    return question_list

@pytest.mark.asyncio
async def test_generate_answer_success_case(user_info, questionnaires):
    # Arrange
    agent = AnswerQuestionAgent(user_info, questionnaires)
    questions = await agent.execute_pipeline()

    assert len(questions) == len(questionnaires)
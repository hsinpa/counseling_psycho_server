import json
from typing import List

import pytest
from pydantic import TypeAdapter

from src.llm_agents.talk_simulation.questionaire.gen_question_prompt import GENERATE_SIMULATION_QUESTION_SYSTEM_PROMPT, \
    GENERATE_SIMULATION_QUESTION_HUMAN_PROMPT, GENERATE_SIMULATION_ADVANCED_QUESTION_HUMAN_PROMPT, \
    GENERATE_SIMULATION_ADVANCED_QUESTION_SYSTEM_PROMPT
from src.llm_agents.talk_simulation.questionaire.gen_question_static import LAST_QUESTION
from src.llm_agents.talk_simulation.questionaire.talk_sim_questionnaire_agent import TalkSimQuestionnaireAgent
from src.llm_agents.talk_simulation.talk_simulation_helper import questionnaire_records_to_string
from src.llm_agents.talk_simulation.talk_simulation_type import GenQuestionParameterInterface, QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.tests.dataset.questionnaires import Slot_Begin_Questionnaire_With_Answer
from src.tests.talk_simulation.test_gen_answer import user_info

@pytest.mark.asyncio
async def test_generate_new_questionnaire_success_case(user_info):
    # Arrange
    q_parameter = GenQuestionParameterInterface(
        system_prompt=GENERATE_SIMULATION_QUESTION_SYSTEM_PROMPT,
        human_prompt=GENERATE_SIMULATION_QUESTION_HUMAN_PROMPT,
        few_shot=LAST_QUESTION,
        process_count=0
    )
    agent = TalkSimQuestionnaireAgent(user_info, q_parameter)

    # Act
    questions = await agent.execute_pipeline()

    # Assert
    assert type(questions) == list and len(questions) > 1

@pytest.mark.asyncio
async def test_generate_iterate_questionnaire_success_case(user_info):
    # Arrange
    question_list_adapter = TypeAdapter(List[List[QuestionType]])
    question_list = question_list_adapter.validate_python([Slot_Begin_Questionnaire_With_Answer])
    question_lens = len(question_list)

    q_parameter = GenQuestionParameterInterface(
        system_prompt=GENERATE_SIMULATION_ADVANCED_QUESTION_SYSTEM_PROMPT,
        human_prompt=GENERATE_SIMULATION_ADVANCED_QUESTION_HUMAN_PROMPT,
        few_shot=questionnaire_records_to_string(question_list),
        process_count=question_lens
    )
    agent = TalkSimQuestionnaireAgent(user_info, q_parameter)

    # Act
    questions = await agent.execute_pipeline()

    # Assert
    assert type(questions) == list and len(questions) > 1
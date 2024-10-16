from typing import List

from pydantic import TypeAdapter

from src.llm_agents.talk_simulation.questionaire.gen_question_prompt import GENERATE_SIMULATION_QUESTION_SYSTEM_PROMPT, \
    GENERATE_SIMULATION_QUESTION_HUMAN_PROMPT, GENERATE_SIMULATION_ADVANCED_QUESTION_SYSTEM_PROMPT, \
    GENERATE_SIMULATION_ADVANCED_QUESTION_HUMAN_PROMPT
from src.llm_agents.talk_simulation.questionaire.gen_question_static import LAST_QUESTION
from src.llm_agents.talk_simulation.questionaire.talk_sim_questionnaire_agent import TalkSimQuestionnaireAgent
from src.llm_agents.talk_simulation.talk_simulation_db_ops import db_ops_save_basic_info, db_ops_save_gen_questionnaire, \
    db_ops_get_simulation_info
from src.llm_agents.talk_simulation.talk_simulation_helper import questionnaire_records_to_string
from src.llm_agents.talk_simulation.talk_simulation_type import GenQuestionParameterInterface, QuestionType
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.service.relation_db.sql_client_interface import SQLClientInterface


class TalkSimulationManager:

    def __init__(self, client: SQLClientInterface):
        self._sql_client = client

    async def exec_new_questionnaire_pipeline(self, user_input: SimulationQuesUserInputType):
        db_ops_save_basic_info(user_input)

        q_parameter = GenQuestionParameterInterface(
            system_prompt=GENERATE_SIMULATION_QUESTION_SYSTEM_PROMPT,
            human_prompt=GENERATE_SIMULATION_QUESTION_HUMAN_PROMPT,
            few_shot=LAST_QUESTION,
            process_count=0
        )

        agent = TalkSimQuestionnaireAgent(user_input, q_parameter)
        questions = await agent.execute_pipeline()

        await db_ops_save_gen_questionnaire(user_input.session_id, questions, process_count_flag=True)

        return questions

    async def exec_iterate_questionnaire_pipeline(self, session_id: str):
        user_info_json = db_ops_get_simulation_info(self._sql_client, session_id)
        user_info: SimulationQuesUserInputType = SimulationQuesUserInputType(**user_info_json)

        question_list_adapter = TypeAdapter(List[List[QuestionType]])
        question_list = question_list_adapter.validate_python(user_info_json['questionnaires'])
        question_lens = len(question_list)

        if question_lens >= 3:
            return question_list[question_lens - 1]

        q_parameter = GenQuestionParameterInterface(
            system_prompt=GENERATE_SIMULATION_ADVANCED_QUESTION_SYSTEM_PROMPT,
            human_prompt=GENERATE_SIMULATION_ADVANCED_QUESTION_HUMAN_PROMPT,
            few_shot=questionnaire_records_to_string(question_list),
            process_count=len(question_list)
        )

        agent = TalkSimQuestionnaireAgent(user_info, q_parameter)
        questions = await agent.execute_pipeline()

        await db_ops_save_gen_questionnaire(session_id, questions, process_count_flag=True)

        return questions
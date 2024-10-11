from src.llm_agents.talk_simulation.questionaire.talk_sim_questionnaire_agent import TalkSimQuestionnaireAgent
from src.llm_agents.talk_simulation.talk_simulation_db_ops import db_ops_save_basic_info, db_ops_save_gen_questionnaire
from src.model.talk_simulation_model import SimulationQuesUserInputType


class TalkSimulationManager:
    def __init__(self, user_input: SimulationQuesUserInputType):
        self._user_input = user_input

    async def execute_questionnaire_pipeline(self):
        db_ops_save_basic_info(self._user_input)

        agent = TalkSimQuestionnaireAgent(self._user_input)
        questions = await agent.execute_pipeline()

        db_ops_save_gen_questionnaire(self._user_input.session_id, questions)

        return questions
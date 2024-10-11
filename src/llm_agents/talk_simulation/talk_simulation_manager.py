from src.llm_agents.talk_simulation.questionaire.talk_sim_questionnaire_agent import TalkSimQuestionnaireAgent
from src.model.talk_simulation_model import SimulationQuesUserInputType


class TalkSimulationManager:
    def __init__(self, user_input: SimulationQuesUserInputType):
        self._user_input = user_input

    async def execute_questionnaire_pipeline(self):
        agent = TalkSimQuestionnaireAgent(self._user_input)
        questions = await agent.execute_pipeline()

        return questions
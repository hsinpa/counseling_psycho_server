import json

from langchain_core.output_parsers import StrOutputParser
from langfuse.callback import CallbackHandler

from src.feature.llm_model import get_gemini_model
from src.feature.talk_simulation.questionaire.gen_question_static import execute_p0_post_effect, \
    execute_p1_post_effect, execute_p2_post_effect
from src.feature.talk_simulation.talk_simulation_helper import basic_info_to_string
from src.feature.talk_simulation.talk_simulation_type import QuestionType, QuestionTypeEnum, \
    GenQuestionParameterInterface
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.utility_method import parse_block


class TalkSimQuestionnaireAgent:

    def __init__(self, user_input: SimulationQuesUserInputType, parameters: GenQuestionParameterInterface):
        self._user_input = user_input
        self._parameters = parameters

    async def _execute_chain(self):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=self._parameters.system_prompt,
            human_prompt_text=self._parameters.human_prompt,
            partial_variables={
                'basic_info': basic_info_to_string(self._user_input),
                'few_shot': self._parameters.few_shot,
                'question_length': 10
            }
        ).with_config({"run_name": 'Talk SIM Questionnaire',
                       "callbacks": [CallbackHandler(user_id='hsinpa')]})

        r = await chain.ainvoke({})

        q_json = json.loads(parse_block('json', r))

        return q_json['questions']

    def _execute_post_effect(self, questions: list[QuestionType], process_count: int):
        if process_count == 0:
            return execute_p0_post_effect(questions)

        if process_count == 1:
            return execute_p1_post_effect(questions)

        return execute_p2_post_effect(questions)


    async def execute_pipeline(self):
        question_str_list = await self._execute_chain()
        questions = list(map(lambda x: QuestionType(content=x) ,question_str_list))

        questions = self._execute_post_effect(questions, self._parameters.process_count)

        return questions
import json

from langchain_core.output_parsers import StrOutputParser
from langfuse.callback import CallbackHandler

from src.llm_agents.llm_model import get_gemini_model
from src.llm_agents.talk_simulation.questionaire.gen_question_prompt import GENERATE_SIMULATION_QUESTION_SYSTEM_PROMPT, \
    GENERATE_SIMULATION_QUESTION_HUMAN_PROMPT
from src.llm_agents.talk_simulation.questionaire.gen_question_static import LAST_QUESTION
from src.llm_agents.talk_simulation.talk_simulation_helper import basic_info_to_string
from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType, QuestionTypeEnum
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.utility_method import parse_block


class TalkSimQuestionnaireAgent:

    def __init__(self, user_input: SimulationQuesUserInputType):
        self._user_input = user_input

    async def _execute_chain(self):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model())
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=GENERATE_SIMULATION_QUESTION_SYSTEM_PROMPT,
            human_prompt_text=GENERATE_SIMULATION_QUESTION_HUMAN_PROMPT,
            partial_variables={
                'basic_info': basic_info_to_string(self._user_input),
                'few_shot': LAST_QUESTION,
                'question_length': 10
            }
        ).with_config({"run_name": 'Talk SIM Questionnaire',
                       "callbacks": [CallbackHandler(user_id='hsinpa')]})

        r = await chain.ainvoke({})

        q_json = json.loads(parse_block('json', r))

        return q_json['questions']

    def _execute_post_effect(self, questions: list[QuestionType]):
        """ Inject static question into the generate questions """
        questions.append(QuestionType(type=QuestionTypeEnum.label,
                                      content="最後想邀請您做一個小小的問卷，請您仔細回想在最近一星期中(包括今天)，這些問題使您感到困擾或苦惱的程度，分別給予0-4分的分數，0分是完全沒有，4分是非常厲害"))

        questions.append(QuestionType(type=QuestionTypeEnum.number, content="感覺緊張不安"))
        questions.append(QuestionType(type=QuestionTypeEnum.number,content="感覺憂鬱"))
        questions.append(QuestionType(type=QuestionTypeEnum.number,content="情緒低落"))
        questions.append(QuestionType(type=QuestionTypeEnum.number,content="覺得比不上別人"))
        questions.append(QuestionType(type=QuestionTypeEnum.number,content="睡眠困難，譬如難以入睡、易醒或早醒"))
        questions.append(QuestionType(type=QuestionTypeEnum.number,content="有自殺的想法"))

        return questions

    async def execute_pipeline(self):
        question_str_list = await self._execute_chain()
        questions = list(map(lambda x: QuestionType(content=x) ,question_str_list))
        questions = self._execute_post_effect(questions)

        return questions
import json

from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.llm_model import get_gemini_model
from src.llm_agents.talk_simulation.answers.answer_question_prompt import ANSWER_QUESTION_SYSTEM_PROMPT, \
    ANSWER_QUESTION_HUMAN_PROMPT
from src.llm_agents.talk_simulation.talk_simulation_helper import basic_info_to_string
from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType, QuestionTypeEnum
from src.model.talk_simulation_model import SimulationQuesUserInputType
from src.utility.simple_prompt_factory import SimplePromptFactory
from langfuse.callback import CallbackHandler

from src.utility.utility_method import parse_block


class AnswerQuestionAgent:
    def __init__(self, user_input: SimulationQuesUserInputType, questionnaires: list[QuestionType]):
        self._user_input = user_input
        self._questionnaires = questionnaires

        self._response_schema = {
            "type": "object",
            "properties": {
                "answers": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    }
                }
            }
        }

    async def _execute_chain(self):
        prompt_factory = SimplePromptFactory(llm_model=get_gemini_model(json_schema=self._response_schema))
        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=ANSWER_QUESTION_SYSTEM_PROMPT,
            human_prompt_text=ANSWER_QUESTION_HUMAN_PROMPT,
            partial_variables={
                'basic_info': basic_info_to_string(self._user_input),
                'questionnaires': self._filtered_questionnaires(self._questionnaires)
            }
        ).with_config({"run_name": 'Answer SIM Questionnaire',
                       "callbacks": [CallbackHandler(user_id='hsinpa')]})

        r = await chain.ainvoke({})

        q_json = json.loads(parse_block('json', r))

        return q_json['answers']

    def _filtered_questionnaires(self, questionnaires: list[QuestionType]):
        new_questionnaires: str = ''
        for index, questionnaire in enumerate(questionnaires):
            if questionnaire.type == QuestionTypeEnum.label:
                break
            new_questionnaires += f'{index + 1}) {questionnaire.content}\n'

        return new_questionnaires

    async def execute_pipeline(self):
        answer_str_list: list[str] = await self._execute_chain()

        for i, answer in enumerate(answer_str_list):
            self._questionnaires[i].answer = answer

        return self._questionnaires
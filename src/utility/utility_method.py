from itertools import islice
from typing import List

from src.llm_agents.theory_prompt import THEORY_REPORT_TEXT, USER_INFO_TEXT
from src.types.router_input_type import AnalysisInputQuestionnaireType, UserMetaType


def chunk(lst: list, n: int):
    it = iter(lst)
    return iter(lambda: tuple(islice(it, n)), ())


def group_user_input_theory_quiz(user_inputs: List[AnalysisInputQuestionnaireType]):
    group_user_theory_quiz = ''
    for user_input in user_inputs:
        custom_text = THEORY_REPORT_TEXT + ''
        custom_text = custom_text.replace('{question}', user_input.questionnaire)
        custom_text = custom_text.replace('{user_answer}', user_input.content)

        group_user_theory_quiz += custom_text
    return group_user_theory_quiz

def group_user_persoanl_info(user_info: UserMetaType):
    custom_text = USER_INFO_TEXT + ''
    custom_text = custom_text.replace('{gender}', user_info.gender)
    custom_text = custom_text.replace('{age}', str(user_info.age))
    custom_text = custom_text.replace('{theme}', user_info.counseling_session)
    custom_text = custom_text.replace('{expect}', user_info.session_expectation)

    return custom_text

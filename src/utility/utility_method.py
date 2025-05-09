import json
import re
from itertools import islice
from typing import List

from src.feature.prompt.theory_prompt import THEORY_REPORT_TEXT, USER_INFO_TEXT
from src.types.router_input_type import AnalysisInputQuestionnaireType, UserMetaType

def clamp(value: int, min_value: int, max_value: int):
    return max(min_value, min(value, max_value))

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

def parse_block(code: str, raw_message: str) -> str:
    try:
        regex_sympy = r'```{code}(?:.|\n)*?```'
        regex_sympy = regex_sympy.replace('{code}', code)

        sympy_codes: list[str] = re.findall(regex_sympy, raw_message)

        raw_llm_msg: str = raw_message

        if len(sympy_codes) > 0:
            raw_llm_msg: str = sympy_codes[0]

        raw_llm_msg = raw_llm_msg.replace(f'```{code}', '')
        raw_llm_msg = raw_llm_msg.replace('```', '')

        return raw_llm_msg
    except Exception as e:
        print(e)

    return raw_message

def parse_json(raw_message: str) -> dict:
    try:
        return json.loads(parse_block('json', raw_message))

    except Exception as e:
        print('parse_json fail to parse ', e)
        raise e

def is_valid_email(email):
    # Email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email matches the pattern
    if re.match(pattern, email):
        return True
    return False

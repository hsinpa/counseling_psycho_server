from src.feature.talk_simulation.talk_simulation_type import QuestionType, QuestionTypeEnum
from src.model.talk_simulation_model import SimulationQuesUserInputType


def basic_info_to_string(basic_info: SimulationQuesUserInputType):

    checkbox_string = ''

    for index, checkbox in enumerate(basic_info.theme_checkboxes):
        checkbox_string += f'{index + 1}). {checkbox.ch_name}\n'

    return f"""\
Age: {basic_info.age}
Gender: {basic_info.gender}
Job: {basic_info.job}
Education: {basic_info.education}

Related theme, sequence matter
{checkbox_string}

[Why pick these theme]
{basic_info.theme_reason}

[User's background]
{basic_info.sorting_reason}\
"""

def questionaries_to_string(questionnaires: list[QuestionType]):
    questionnaires_text = ''

    for i, q in enumerate(questionnaires):
        if q.type == QuestionTypeEnum.text:
            questionnaires_text += f'Question. {q.content}\n'
            questionnaires_text += f'Answer:\n{q.answer}\n\n'

        if q.type == QuestionTypeEnum.label:
            questionnaires_text += f'** {q.content}\n'

        if q.type == QuestionTypeEnum.number:
            questionnaires_text += f'{q.content}: {q.answer}\n'

    return questionnaires_text

def questionnaire_records_to_string(questionnaire_records: list[list[QuestionType]]):
    whole_questionnaires_text = ''

    for i, q in enumerate(questionnaire_records):
        whole_questionnaires_text += f"** Survey: {i+1} **\n"
        whole_questionnaires_text += questionaries_to_string(q) +'\n\n'

    return whole_questionnaires_text
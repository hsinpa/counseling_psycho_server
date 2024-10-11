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

[Why sort this way]
{basic_info.sorting_reason}\
"""

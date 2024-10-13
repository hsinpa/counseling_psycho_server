import json
from src.model.multi_theory_model import MultiTheoryDataType, MultiTheoriesDataType


def psycho_theory_to_text(theory_array: list[MultiTheoryDataType]):
    text = ''
    for i, x in enumerate(theory_array):
        text += f'** {x.name}, Index {i}\n'
        text += '\n'.join(x.dimension)
        text += '\n\n'
    return text


def psycho_theory_json():
    with open("./src/data/theory_definition.json", encoding='utf-8') as f:
        psycho_theories = json.load(f)
        return psycho_theories


def psycho_theory_dict():
    theory_dict = {}
    with open("./src/data/theory_definition.json", encoding='utf-8') as f:
        psycho_theories = json.load(f)
        for x in psycho_theories['theory']:
            theory_dict[x['id']] = MultiTheoryDataType(**x)

        return theory_dict


GLOBAL_PSYCHO_THEORY_ARRAY = MultiTheoriesDataType(**psycho_theory_json())
GLOBAL_PSYCHO_THEORY_DICT: dict = psycho_theory_dict()
GLOBAL_PSYCHO_THEORY_TEXT: str = psycho_theory_to_text(GLOBAL_PSYCHO_THEORY_ARRAY.theory)
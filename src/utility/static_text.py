import json
from enum import Enum

from src.model.multi_theory_model import MultiTheoryDataType

OpenAI_Model_4o = 'gpt-4o'
OpenAI_Model_3_5 = 'gpt-3.5-turbo'
OpenAI_Model_4o_mini = 'gpt-4o-mini'
Gemini_Model_1_5 = 'gemini-1.5-flash'


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

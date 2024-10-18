import operator
from typing import TypedDict, Annotated

from src.model.multi_theory_model import MultiTheoryDataType


class MixTheoryGraphState(TypedDict):
    selected_questionnaire_list: Annotated[list[MultiTheoryDataType], operator.add]
    user_info: str
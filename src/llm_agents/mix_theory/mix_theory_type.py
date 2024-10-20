import operator
from typing import TypedDict, Annotated

from src.model.multi_theory_model import MultiTheoryDataType


class MixTheoryGraphState(TypedDict):
    selected_theory_list: Annotated[list[MultiTheoryDataType], operator.add]
    user_info: str

    analysis_report: str
    question_report: str
    strategy_report: str
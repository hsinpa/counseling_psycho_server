from typing_extensions import TypedDict

from src.model.multi_theory_model import MultiTheoryDataType


class ReportTheoryGraphState(TypedDict):
    questionnaire_full_text: str
    selected_questionnaire_list: list[MultiTheoryDataType]
    report: str
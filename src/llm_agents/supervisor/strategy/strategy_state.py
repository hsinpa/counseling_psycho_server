from typing import TypedDict

class StrategyState(TypedDict):
    transcribe_text: str
    therapy_issue_objective: str
    cognitive_model: str

    core_intermediate_belief: str
    mean_of_AT: str

    relevant_history_precipitants: str
    coping_strategy: str

from typing import TypedDict

class StrategyState(TypedDict):
    transcribe_text: str
    therapy_issue_objective: str
    next_session_therapy_direction: str
    treatment_effectiveness: str

    client_situations: str
    cognitive_model: str

    core_intermediate_belief: str
    mean_of_AT: str

    relevant_history_precipitants: str
    coping_strategy: str
    situations_relevant_to_issue: str
    knowledge_graph_issue: str

    next_therapy_goal: str
    treatment_strategy: str

from typing import TypedDict, List

class CaseConceptState(TypedDict):
    transcribe_text: str

    treatment_framework: str
    therapy_issue_objective: str
    methods_and_techniques: str

    treatment_progress: str
    therapy_outcome: str

    treatment_effectiveness: str

    next_session_therapy_direction: str
    short_to_mid_term_therapy_Direction: str
    long_term_therapy_direction: str

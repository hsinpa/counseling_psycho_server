from typing import TypedDict, List

class CaseTreatmentState(TypedDict):
    # Input
    transcribe_text: str
    treatment_framework: str
    therapy_issue_objective: str
    knowledge_graph_issue: str

    # Output
    case_treatment_information: str
    case_treatment_strategy: str
    case_phase_evaluation_criteria: str

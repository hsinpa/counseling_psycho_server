from typing import TypedDict, List

class PrerequisiteState(TypedDict):
    # Input
    transcribe_text: str

    # Output
    treatment_framework: str
    therapy_issue_objective: str
from typing import TypedDict

class HomeworkState(TypedDict):
    transcribe_text: str
    therapy_issue_objective: str
    knowledge_graph_issue: str

    action_plan: str
    homework_assignment: str
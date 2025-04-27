from typing import List

from pydantic import BaseModel

Table = ''

DB_TRANSCRIPT_TABLE = 'transcript'
DB_SUPERVISOR_REPORT_TABLE = 'supervisor_report'


# region Issue and Treatment strategies
class TherapyIssueObjective(BaseModel):
    title: str
    objective: str

class TreatmentStrategy(BaseModel):
    issue: str
    goal: str
    treatment_direction: str
    depth: str
    intervention_techniques: List[str]
    improvement_methods: List[str]

class IssueTreatmentStrategy(BaseModel):
    therapy_issue_objective: TherapyIssueObjective
    treatment_strategy: TreatmentStrategy
    next_therapy_goal: str
    title: str
    range: List[str]

# endregion

# region Homework
class SingleHomework(BaseModel):
    title: str
    goal: str
    task: str
    steps: list[str]

class HomeworkAssignment(BaseModel):
    homeworks: list[SingleHomework]
    reflection_questions: list[str]
# endregion

# region Case Conceptualization
class MeanOfAT(BaseModel):
    situation: str
    mean_of_AT: str

class RelevantHistoryPrecipitant(BaseModel):
    relevant_life_history: list[str]
    precipitants: list[str]

class CoreBelief(BaseModel):
    core_belief_type: str
    explanation: str
    client_core_belief: list[str]

class IntermediateBelief(BaseModel):
    intermediate_belief: str
    positive_assumption: str
    negative_assumption: str

class CoreIntermediateBelief(BaseModel):
    core_beliefs: list[CoreBelief]
    intermediate_beliefs: list[IntermediateBelief]

class CopingStrategy(BaseModel):
    summaries: List[str]
    rules: List[str]
    attitudes: List[str]

class SingleCognitiveModel(BaseModel):
    situation: str
    automatic_thought: str
    emotion: str
    physiological_response: str
    behavior: str

class CaseConceptualizationModel(BaseModel):
    core_intermediate_belief: CoreIntermediateBelief
    relevant_history_precipitants: RelevantHistoryPrecipitant
    mean_of_AT: list[MeanOfAT]
    cognitive_model: list[SingleCognitiveModel]
    coping_strategy: CopingStrategy

# endregion

class SupervisorAnalysisRespModel(BaseModel):
    case_conceptualization: CaseConceptualizationModel
    homework_assignment: HomeworkAssignment
    issue_treatment_strategies: List[IssueTreatmentStrategy]
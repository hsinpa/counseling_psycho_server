from typing import List

from pydantic import BaseModel

Table = ''

DB_TRANSCRIPT_TABLE = 'transcript'
DB_SUPERVISOR_REPORT_TABLE = 'supervisor_report'


# region Issue and Treatment strategies
class TreatmentEvaluation(BaseModel):
    phase_specific_evaluation_criteria: str
    challenge: str
    emotional_disturbance: bool
    recommended_step_to_swift_to: str
    recommended_swift_step_index: int

class TreatmentStep(BaseModel):
    title: str
    therapeutic_goal: str
    explanation_of_technique: str

class IssueTreatmentStrategy(BaseModel):
    treatment_evaluations: list[TreatmentEvaluation]
    treatment_steps: list[TreatmentStep]
    issue: str
    goal: str
    focus_of_stepped_care: str

# endregion

# region Homework
class SingleHomeworkStep(BaseModel):
    plan: str
    example: str

class SingleHomework(BaseModel):
    title: str
    goal: str
    task: str
    steps: list[SingleHomeworkStep]

class HomeworkAssignment(BaseModel):
    homeworks: list[SingleHomework]
    reflection_questions: list[str]
# endregion

# region Case Conceptualization
class MeanOfAT(BaseModel):
    situation: str
    meaning_of_AT: str

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
    title: str
    summary: str
    rule: str
    attitude: str

class SingleCognitiveModel(BaseModel):
    situation: str
    automatic_thought: str
    emotion: str
    physiological_response: str
    behavior: str

class CaseConceptualizationModel(BaseModel):
    core_intermediate_belief: CoreIntermediateBelief
    relevant_history_precipitants: RelevantHistoryPrecipitant
    meaning_of_AT: list[MeanOfAT]
    cognitive_model: list[SingleCognitiveModel]
    coping_strategies: list[CopingStrategy]

# endregion

class SupervisorAnalysisRespModel(BaseModel):
    case_conceptualization: CaseConceptualizationModel
    homework_assignment: HomeworkAssignment
    issue_treatment_strategies: List[IssueTreatmentStrategy]

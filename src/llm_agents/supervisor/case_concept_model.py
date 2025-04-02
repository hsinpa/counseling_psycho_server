from typing import List

from pydantic import BaseModel

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
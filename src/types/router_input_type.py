from enum import Enum
from typing import Text, List

from pydantic import BaseModel

class AnalysisInputQuestionnaireType(BaseModel):
    questionnaire_id: str
    questionnaire: str
    content: str

class AnalysisInputQuestionnairesType(BaseModel):
    content: List[AnalysisInputQuestionnaireType]


class TheoryEnum(str, Enum):
    object_relation_theory = 'object_relation_theory'
    somatic_experience = 'somatic_experience'
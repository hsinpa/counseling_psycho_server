from enum import Enum
from typing import Text, List, Optional

from pydantic import BaseModel

from src.model.multi_theory_model import StreamUserInput


class TheoryEnum(str, Enum):
    object_relation_theory = 'object_relation_theory'
    somatic_experience = 'somatic_experience'
    cognitive_behavior = 'cognitive_behavior'


class UserMetaType(BaseModel):
    gender: str
    age: int
    counseling_session: str
    session_expectation: str


class AnalysisInputQuestionnaireType(BaseModel):
    questionnaire_id: str
    questionnaire: str
    content: str


class AnalysisInputQuestionnairesType(StreamUserInput):
    theory: TheoryEnum
    user_meta: UserMetaType
    question_answer_pairs: List[AnalysisInputQuestionnaireType]


class InputMediaStrategyType(StreamUserInput):
    theory: TheoryEnum
    content: str

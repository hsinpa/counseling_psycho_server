from typing import List

from pydantic import BaseModel


class QuestionnaireRespType(BaseModel):
    id: str
    content: str


class QuestionnairesRespType(BaseModel):
    questions: List[QuestionnaireRespType]


class CognitiveQuestionRespType(BaseModel):
    id: str
    content: str
    type: str


class CognitiveQuestionsRespType(BaseModel):
    questions: List[CognitiveQuestionRespType]
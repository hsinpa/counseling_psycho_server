from typing import List

from pydantic import BaseModel


class QuestionnaireRespType(BaseModel):
    id: str
    content: str


class QuestionnairesRespType(BaseModel):
    questions: List[QuestionnaireRespType]

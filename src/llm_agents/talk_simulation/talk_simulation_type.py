from enum import Enum
from typing import TypedDict, Optional

from pydantic import BaseModel, Field


class QuestionTypeEnum(str, Enum):
    text = 'text'
    label = 'label'
    number = 'number'

class GenQuestionParameterInterface(BaseModel):
    system_prompt: str
    human_prompt: str
    few_shot: str
    process_count: int

class QuestionType(BaseModel):
    type: QuestionTypeEnum = Field(default=QuestionTypeEnum.text)
    content: str
    answer: Optional[str] = Field(default='')

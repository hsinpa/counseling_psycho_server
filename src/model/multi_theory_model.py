from pydantic import BaseModel


class StreamUserInput(BaseModel):
    user_id: str
    session_id: str


class MultiTheoryInputType(StreamUserInput):
    theory_id: str
    content: str


class MultiTheoryDataType(BaseModel):
    id: str
    name: str
    dimension: list[str]


class MultiTheoriesDataType(BaseModel):
    theory: list[MultiTheoryDataType]

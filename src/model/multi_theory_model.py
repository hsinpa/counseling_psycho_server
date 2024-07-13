from pydantic import BaseModel


class StreamUserInput(BaseModel):
    user_id: str
    session_id: str


class MultiTheoryInputType(StreamUserInput):
    theory_id: str
    content: str


class MixTheoryInputType(StreamUserInput):
    theory_id: list[str]
    content: str

class MixTheoryRespType(BaseModel):
    id: str
    theory_id: list[str]
    theory_name: list[str]
    content: str

class MultiTheoryDataType(BaseModel):
    id: str
    name: str
    dimension: list[str]


class MultiTheoriesDataType(BaseModel):
    theory: list[MultiTheoryDataType]


class MultiTheoryRespType(BaseModel):
    id: str
    theory_id: str
    theory_name: str
    content: str

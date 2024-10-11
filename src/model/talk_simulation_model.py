from pydantic import BaseModel

class SimulationThemeCheckboxType(BaseModel):
    id: str
    ch_name: str
    en_name: str

class SimulationThemeCheckboxesType(BaseModel):
    checkboxes: list[SimulationThemeCheckboxType]


class SimulationQuesUserInputType(BaseModel):
    age: int
    gender: str
    job: str
    education: str
    theme_checkboxes: list[SimulationThemeCheckboxType]

    theme_reason: str
    sorting_reason: str
    session_id: str
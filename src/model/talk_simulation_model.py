from pydantic import BaseModel

class SimulationThemeCheckboxType(BaseModel):
    id: str
    ch_name: str
    en_name: str

class SimulationThemeCheckboxesType(BaseModel):
    checkboxes: list[SimulationThemeCheckboxType]

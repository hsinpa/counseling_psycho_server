import json
from typing import Optional

from pydantic import BaseModel

from src.llm_agents.talk_simulation.talk_simulation_type import QuestionType


class SimulationThemeCheckboxType(BaseModel):
    id: str
    ch_name: str
    en_name: str

class SimulationThemeCheckboxesType(BaseModel):
    checkboxes: list[SimulationThemeCheckboxType]

class SimulationReportInput(BaseModel):
    session_id: str
    socket_id: str
    questionnaires: list[QuestionType]

class SimulationQuesUserInputType(BaseModel):
    age: int
    gender: str
    job: str
    education: str
    theme_checkboxes: list[SimulationThemeCheckboxType]

    theme_reason: str
    sorting_reason: str
    session_id: Optional[str] = None

GLOBAL_SIMULATION_CHECKBOX_DICT: dict = {}
GLOBAL_SIMULATION_CHECKBOXES: SimulationThemeCheckboxesType

try:
    with open("./src/data/talk_simulation_checkboxes.json", encoding='utf-8') as f:
        checkboxes_array = json.load(f)
        GLOBAL_SIMULATION_CHECKBOXES = SimulationThemeCheckboxesType(**checkboxes_array)

        for checkbox in checkboxes_array['checkboxes']:
            GLOBAL_SIMULATION_CHECKBOX_DICT[checkbox["id"]] = checkbox
except Exception as e:
    print('talk_simulation_checkboxes.json fail to load')

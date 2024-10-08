import json

from fastapi import APIRouter, HTTPException, BackgroundTasks

from src.model.talk_simulation_model import SimulationThemeCheckboxesType, SimulationQuesUserInputType

router = APIRouter(prefix="/api/talk_simulation", tags=["talk_simulation"])


@router.get("/get_simulation_checkboxes")
def get_simulation_checkboxes() -> SimulationThemeCheckboxesType:
    try:
        with open("./src/data/talk_simulation_checkboxes.json", encoding='utf-8') as f:
            checkboxes_array = json.load(f)
        return SimulationThemeCheckboxesType(**checkboxes_array)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Checkbox not found")

@router.post("/gen_simulation_quiz")
def gen_simulation_quiz(user_input: SimulationQuesUserInputType):
    try:

        pass
    except Exception as e:
        raise HTTPException(status_code=404, detail="Checkbox not found")
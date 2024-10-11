import json

from fastapi import APIRouter, HTTPException, BackgroundTasks

from src.llm_agents.talk_simulation.talk_simulation_db_ops import db_ops_get_simulation_info
from src.llm_agents.talk_simulation.talk_simulation_manager import TalkSimulationManager
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

@router.get("/get_simulation_talk/{session_id}")
async def gen_simulation_quiz(session_id: str):
    try:
        print(session_id)
        return db_ops_get_simulation_info(session_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Session do not exist")


@router.post("/gen_simulation_quiz")
async def gen_simulation_quiz(user_input: SimulationQuesUserInputType):
    try:
        talk_sim_manager = TalkSimulationManager(user_input)

        questions = await talk_sim_manager.execute_questionnaire_pipeline()

        print(questions)

        return questions
    except Exception as e:
        raise HTTPException(status_code=404, detail="Checkbox not found")


@router.post("/gen_simulation_answer")
async def gen_simulation_answer(user_input: SimulationQuesUserInputType):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=404, detail="Checkbox not found")
from fastapi import APIRouter, HTTPException, BackgroundTasks

from src.llm_agents.talk_simulation.answers.answer_question_manager import AnswerQuestionManager
from src.llm_agents.talk_simulation.detail_report.report_theory_manager import ReportTheoryManager
from src.llm_agents.talk_simulation.talk_simulation_db_ops import db_ops_get_simulation_external_view, \
    db_ops_save_gen_questionnaire
from src.llm_agents.talk_simulation.questionaire.talk_sim_questionnaire_manager import TalkSimulationManager
from src.model.talk_simulation_model import SimulationThemeCheckboxesType, SimulationQuesUserInputType, \
    GLOBAL_SIMULATION_CHECKBOXES, SimulationQuizInput, StreamSimulationInput

router = APIRouter(prefix="/api/talk_simulation", tags=["talk_simulation"])


@router.get("/get_simulation_checkboxes")
def get_simulation_checkboxes() -> SimulationThemeCheckboxesType:
    return GLOBAL_SIMULATION_CHECKBOXES

@router.get("/get_simulation_talk/{session_id}")
async def get_simulation_talk(session_id: str):
    # try:
    #     print(session_id)
    return db_ops_get_simulation_external_view(session_id)
    # except Exception as e:
    #     raise HTTPException(status_code=404, detail="Session do not exist")


@router.post("/gen_simulation_quiz")
async def gen_simulation_quiz(user_input: SimulationQuesUserInputType):
    # try:
    talk_sim_manager = TalkSimulationManager()

    questions = await talk_sim_manager.exec_new_questionnaire_pipeline(user_input)

    return questions
    # except Exception as e:
    #     raise HTTPException(status_code=404, detail="Checkbox not found")

@router.post("/iterate_simulation_quiz/{session_id}")
async def iterate_simulation_quiz(session_id: str):
    # try:
    talk_sim_manager = TalkSimulationManager()

    questions = await talk_sim_manager.exec_iterate_questionnaire_pipeline(session_id)

    return questions


    # except Exception as e:
    #     raise HTTPException(status_code=404, detail="Checkbox not found")


@router.post("/gen_simulation_answer/{session_id}")
async def gen_simulation_answer(session_id: str):
    try:
        answer_sim_manager = AnswerQuestionManager(session_id)

        return await answer_sim_manager.execute_questionnaire_pipeline()

    except Exception as e:
        raise HTTPException(status_code=404, detail={e})

@router.put("/update_simulation_quiz")
async def update_simulation_quiz(user_input: SimulationQuizInput):
    # try:
    db_ops_save_gen_questionnaire(user_input.session_id, user_input.questionnaires)

    return {"status": True}
    # except Exception as e:
    #     raise HTTPException(status_code=404, detail="Session id do not exist")

@router.post("/gen_simulation_report")
async def gen_simulation_report(user_input: StreamSimulationInput):
    answer_sim_manager = ReportTheoryManager(user_input)

    return await answer_sim_manager.execute_report_pipeline()

@router.post("/sgen_simulation_report")
def sgen_simulation_report(user_input: StreamSimulationInput, background_tasks: BackgroundTasks):
    background_tasks.add_task(gen_simulation_report, user_input=user_input)

    return {'session_id': user_input.session_id, 'socket_id': user_input.socket_id}
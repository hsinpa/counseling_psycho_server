import json

from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.feature.report_features import output_individual_strategy, output_theory_report
from src.feature.prompt.theory_prompt import INDIVIDUAL_THEORY_REPORT_PROMPT, MEDIATION_STRATEGY_REPORT_PROMPT, \
    COGNITIVE_BEHAVIOR_REPORT_PROMPT, COGNITIVE_INDIVIDUAL_REPORT_PROMPT
from src.model.questionnaire_model import QuestionnairesRespType, QuestionnaireRespType, CognitiveQuestionsRespType
from src.types.router_input_type import AnalysisInputQuestionnairesType, InputMediaStrategyType

router = APIRouter(prefix="/api/questionnaire", tags=["questionnaire"])


@router.get("/get_cognitive_questions")
def get_theory_questions() -> CognitiveQuestionsRespType:
    try:
        with open("./src/data/cognitive_behavior_questions.json", encoding='utf-8') as f:
            psycho_theories = json.load(f)
        return CognitiveQuestionsRespType(**psycho_theories)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_cognitive_report")
async def output_cognitive_report(analysis_input: AnalysisInputQuestionnairesType, background_tasks: BackgroundTasks) -> QuestionnaireRespType:
    try:
        background_tasks.add_task(output_theory_report, analysis_input, COGNITIVE_BEHAVIOR_REPORT_PROMPT)
        return QuestionnaireRespType(id=analysis_input.session_id, content='')
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_cognitive_individual")
async def output_cognitive_individual(p_input: InputMediaStrategyType, background_tasks: BackgroundTasks) -> QuestionnaireRespType:
    try:
        background_tasks.add_task(output_individual_strategy, p_input, COGNITIVE_INDIVIDUAL_REPORT_PROMPT)
        return QuestionnaireRespType(id=p_input.session_id, content='')
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.get("/get_theory_questions")
def get_theory_questions() -> QuestionnairesRespType:
    try:
        with open("./src/data/psycho_theory_questions.json", encoding='utf-8') as f:
            psycho_theories = json.load(f)
        return QuestionnairesRespType(**psycho_theories)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_theory_report")
async def route_output_theory_report(analysis_input: AnalysisInputQuestionnairesType, background_tasks: BackgroundTasks) -> QuestionnaireRespType:
    try:
        background_tasks.add_task(output_theory_report, analysis_input, INDIVIDUAL_THEORY_REPORT_PROMPT)

        return QuestionnaireRespType(id=analysis_input.session_id, content='')
        # return await output_theory_report(analysis_input=analysis_input,
        #                                   prompt_template=INDIVIDUAL_THEORY_REPORT_PROMPT)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_mediation_strategy")
async def output_mediation_strategy(user_report: InputMediaStrategyType, background_tasks: BackgroundTasks) -> QuestionnaireRespType:
    try:
        background_tasks.add_task(output_individual_strategy, user_report, MEDIATION_STRATEGY_REPORT_PROMPT)

        return QuestionnaireRespType(id=user_report.session_id, content='')
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")

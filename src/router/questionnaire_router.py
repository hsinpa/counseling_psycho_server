import json
import uuid

from fastapi import APIRouter, HTTPException
from langchain_core.messages import AIMessageChunk
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.report_features import output_individual_strategy, output_theory_report
from src.llm_agents.theory_prompt import INDIVIDUAL_THEORY_REPORT_PROMPT, MEDIATION_STRATEGY_REPORT_PROMPT, \
    COGNITIVE_BEHAVIOR_REPORT_PROMPT, COGNITIVE_INDIVIDUAL_REPORT_PROMPT
from src.model.questionnaire_model import QuestionnairesRespType, QuestionnaireRespType, CognitiveQuestionsRespType
from src.types.router_input_type import TheoryEnum, AnalysisInputQuestionnairesType, InputMediaStrategyType

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


@router.get("/get_cognitive_questions")
def get_theory_questions() -> CognitiveQuestionsRespType:
    try:
        with open("./src/data/cognitive_behavior_questions.json", encoding='utf-8') as f:
            psycho_theories = json.load(f)
        return CognitiveQuestionsRespType(**psycho_theories)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_cognitive_report")
async def output_cognitive_report(analysis_input: AnalysisInputQuestionnairesType) -> QuestionnaireRespType:
    try:
        return await output_theory_report(analysis_input=analysis_input,
                                          prompt_template=COGNITIVE_BEHAVIOR_REPORT_PROMPT)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_cognitive_individual")
async def output_cognitive_individual(input: InputMediaStrategyType) -> QuestionnaireRespType:
    try:
        return await output_individual_strategy(user_input=input, prompt_template=COGNITIVE_INDIVIDUAL_REPORT_PROMPT)
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
async def route_output_theory_report(analysis_input: AnalysisInputQuestionnairesType) -> QuestionnaireRespType:
    try:
        return await output_theory_report(analysis_input=analysis_input,
                                          prompt_template=INDIVIDUAL_THEORY_REPORT_PROMPT)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_mediation_strategy")
async def output_mediation_strategy(user_report: InputMediaStrategyType) -> QuestionnaireRespType:
    try:
        return await output_individual_strategy(user_report, MEDIATION_STRATEGY_REPORT_PROMPT)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")

import json
import uuid

from fastapi import APIRouter, HTTPException
from langchain_core.messages import AIMessageChunk
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.theory_prompt import INDIVIDUAL_THEORY_REPORT_PROMPT, MEDIATION_STRATEGY_REPORT_PROMPT, \
    COGNITIVE_BEHAVIOR_REPORT_PROMPT, COGNITIVE_INDIVIDUAL_REPORT_PROMPT
from src.model.questionnaire_model import QuestionnairesRespType, QuestionnaireRespType, CognitiveQuestionsRespType
from src.types.router_input_type import TheoryEnum, AnalysisInputQuestionnairesType, InputMediaStrategyType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.utility_method import group_user_input_theory_quiz, group_user_persoanl_info

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
# try:
    user_personal_info = group_user_persoanl_info(analysis_input.user_meta)
    user_theory_report = group_user_input_theory_quiz(analysis_input.question_answer_pairs)

    factory = SimplePromptFactory()

    chain = factory.create_chain(output_parser=StrOutputParser(),
                         human_prompt_text=COGNITIVE_BEHAVIOR_REPORT_PROMPT,
                         partial_variables={'content': user_personal_info + '\n' + user_theory_report})

    results = ''
    async for chunk in chain.astream({"topic": "parrot"}):
        results = results + chunk

    return QuestionnaireRespType(id=str(uuid.uuid4()), content=results)
    # except Exception as e:
    #     raise HTTPException(status_code=404, detail="Agent not found")

@router.post("/output_cognitive_individual")
async def output_cognitive_individual(input: InputMediaStrategyType) -> QuestionnaireRespType:
    try:
        factory = SimplePromptFactory()

        chain = factory.create_chain(output_parser=StrOutputParser(),
                                     human_prompt_text=COGNITIVE_INDIVIDUAL_REPORT_PROMPT,
                                     partial_variables={'content': input.content})
        result = await chain.ainvoke({})

        return QuestionnaireRespType(id=str(uuid.uuid4()), content=result)
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
async def output_theory_report(analysis_input: AnalysisInputQuestionnairesType) -> QuestionnaireRespType:
    try:
        user_personal_info = group_user_persoanl_info(analysis_input.user_meta)
        user_theory_report = group_user_input_theory_quiz(analysis_input.question_answer_pairs)

        factory = SimplePromptFactory()

        chain = factory.create_chain(output_parser=StrOutputParser(),
                             human_prompt_text=INDIVIDUAL_THEORY_REPORT_PROMPT,
                             partial_variables={'content': user_personal_info + '\n' + user_theory_report})
        result = await chain.ainvoke({})

        return QuestionnaireRespType(id=str(uuid.uuid4()), content=result)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")

@router.post("/output_mediation_strategy")
async def output_mediation_strategy(input: InputMediaStrategyType) -> QuestionnaireRespType:
    try:
        factory = SimplePromptFactory()

        chain = factory.create_chain(output_parser=StrOutputParser(),
                                     human_prompt_text=MEDIATION_STRATEGY_REPORT_PROMPT,
                                     partial_variables={'content': input.content})
        result = await chain.ainvoke({})

        return QuestionnaireRespType(id=str(uuid.uuid4()), content=result)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")
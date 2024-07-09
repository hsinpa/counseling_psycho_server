import json

from fastapi import APIRouter, HTTPException

from src.model.multi_theory_model import MultiTheoriesDataType, MultiTheoryInputType
from src.model.questionnaire_model import CognitiveQuestionsRespType, QuestionnaireRespType
from src.types.router_input_type import AnalysisInputQuestionnairesType

router = APIRouter(prefix="/multi_theory", tags=["multi_theory"])

pyscho_theory_dict = {}
with open("./src/data/theory_definition.json", encoding='utf-8') as f:
    psycho_theories = json.load(f)
    for x in psycho_theories['theory']:
        pyscho_theory_dict[x['id']] = x

@router.get("/get_multi_theory")
def get_multi_theory() -> MultiTheoriesDataType:
    try:
        return MultiTheoriesDataType(**psycho_theories)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")

@router.post("/output_multi_theory_report")
async def output_multi_theory_report(analysis_input: MultiTheoryInputType) -> QuestionnaireRespType:

    if analysis_input.theory in pyscho_theory_dict:



        pass

    return QuestionnaireRespType(id=analysis_input.session_id, content='')
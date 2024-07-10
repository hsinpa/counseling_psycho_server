import json

from fastapi import APIRouter, HTTPException
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.multi_theory_prompt import MULTI_THEORY_CREATION_PROMPT
from src.model.multi_theory_model import MultiTheoriesDataType, MultiTheoryInputType, MultiTheoryDataType, \
    MultiTheoryRespType
from src.model.questionnaire_model import CognitiveQuestionsRespType, QuestionnaireRespType
from src.types.router_input_type import AnalysisInputQuestionnairesType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer

router = APIRouter(prefix="/multi_theory", tags=["multi_theory"])

pyscho_theory_dict = {}
with open("./src/data/theory_definition.json", encoding='utf-8') as f:
    psycho_theories = json.load(f)
    for x in psycho_theories['theory']:
        pyscho_theory_dict[x['id']] = MultiTheoryDataType(**x)

@router.get("/get_multi_theory")
def get_multi_theory() -> MultiTheoriesDataType:
    try:
        return MultiTheoriesDataType(**psycho_theories)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")

@router.post("/output_multi_theory_report")
async def output_multi_theory_report(analysis_input: MultiTheoryInputType) -> MultiTheoryRespType:

    if analysis_input.theory_id in pyscho_theory_dict:
        theory_obj: MultiTheoryDataType = pyscho_theory_dict[analysis_input.theory_id]
        simple_factory = SimplePromptFactory(trace_langfuse=True, trace_name='Multi_Theory_Report')
        simple_streamer = SimplePromptStreamer(user_id=analysis_input.user_id, session_id=analysis_input.session_id)

        print(theory_obj)
        dimension_concat = '\n'.join(theory_obj.dimension)

        chain = simple_factory.create_chain(output_parser=StrOutputParser(),
                                     human_prompt_text=MULTI_THEORY_CREATION_PROMPT,
                                     partial_variables={'theory': theory_obj.name,
                                                        'dimension': dimension_concat,
                                                        'personal_info': analysis_input.content})

        result = await simple_streamer.execute(chain=chain)

        return MultiTheoryRespType(id=analysis_input.session_id, content=result, theory_name=theory_obj.name, theory_id=analysis_input.theory_id)

    return MultiTheoryRespType(id=analysis_input.session_id, content='', theory_name='', theory_id='')
import json

from fastapi import APIRouter, HTTPException
from langchain_core.output_parsers import StrOutputParser

from src.llm_agents.llm_model import LLMModel
from src.llm_agents.multi_theory_prompt import MULTI_THEORY_CREATION_PROMPT, MIX_THEORY_CREATION_PROMPT
from src.model.multi_theory_model import MultiTheoriesDataType, MultiTheoryInputType, MultiTheoryDataType, \
    MultiTheoryRespType, MixTheoryInputType, MixTheoryRespType
from src.model.questionnaire_model import CognitiveQuestionsRespType, QuestionnaireRespType
from src.types.router_input_type import AnalysisInputQuestionnairesType
from src.utility.simple_prompt_factory import SimplePromptFactory
from src.utility.simple_prompt_streamer import SimplePromptStreamer
from src.utility.static_text import Gemini_Model_1_5, OpenAI_Model_3_5

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
        simple_factory = SimplePromptFactory(trace_langfuse=True, trace_name='Multi_Theory_Report',
                                             model_name=OpenAI_Model_3_5, llm_model=LLMModel.OpenAI)
        simple_streamer = SimplePromptStreamer(user_id=analysis_input.user_id, session_id=analysis_input.session_id)

        print(theory_obj)
        dimension_concat = '\n'.join(theory_obj.dimension)

        chain = simple_factory.create_chain(output_parser=StrOutputParser(),
                                            human_prompt_text=MULTI_THEORY_CREATION_PROMPT,
                                            partial_variables={'theory': theory_obj.name,
                                                               'dimension': dimension_concat,
                                                               'personal_info': analysis_input.content})

        result = await simple_streamer.execute(chain=chain)

        return MultiTheoryRespType(id=analysis_input.session_id, content=result, theory_name=theory_obj.name,
                                   theory_id=analysis_input.theory_id)

    return MultiTheoryRespType(id=analysis_input.session_id, content='', theory_name='', theory_id='')


@router.post("/output_mix_theory_report")
async def output_mix_theory_report(analysis_input: MixTheoryInputType) -> MixTheoryRespType:
    theory_dimension_list: list[str] = []
    theory_name_list: list[str] = []
    print(analysis_input)
    for p_theory in analysis_input.theory_id:
        if p_theory in pyscho_theory_dict:
            theory = pyscho_theory_dict[p_theory]

            theory_name_list.append(theory.name)
            theory_dimension_list.append('. '.join(theory.dimension) + '\n')

    simple_factory = SimplePromptFactory(trace_langfuse=True, trace_name='Multi_Theory_Report',
                                         model_name=OpenAI_Model_3_5, llm_model=LLMModel.OpenAI)
    chain = simple_factory.create_chain(output_parser=StrOutputParser(),
                                        human_prompt_text=MIX_THEORY_CREATION_PROMPT,
                                        partial_variables={'theory': ','.join(theory_name_list),
                                                           'dimension': ';'.join(theory_dimension_list),
                                                           'personal_info': analysis_input.content})
    result = await chain.ainvoke({})

    return MixTheoryRespType(id=analysis_input.session_id,
                             content=result,
                             theory_name=theory_name_list,
                             theory_id=analysis_input.theory_id)

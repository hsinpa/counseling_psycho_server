import json

from fastapi import APIRouter, HTTPException, BackgroundTasks

from src.llm_agents.report_features import stream_mix_theory_report, stream_multi_theory_report
from src.model.multi_theory_model import MultiTheoriesDataType, MultiTheoryInputType, MultiTheoryDataType, \
    MultiTheoryRespType, MixTheoryInputType, MixTheoryRespType
from src.utility.static_text import psycho_theory_dict, psycho_theory_json
from src.websocket.websocket_manager import get_websocket

router = APIRouter(prefix="/api/multi_theory", tags=["multi_theory"])
socket_manager = get_websocket()

@router.get("/get_multi_theory")
def get_multi_theory() -> MultiTheoriesDataType:
    try:
        return MultiTheoriesDataType(**psycho_theory_json())
    except Exception as e:
        raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/output_multi_theory_report")
async def output_multi_theory_report(analysis_input: MultiTheoryInputType,
                                     background_tasks: BackgroundTasks) -> MultiTheoryRespType:
    background_tasks.add_task(stream_multi_theory_report, analysis_input)

    return MultiTheoryRespType(id=analysis_input.session_id,
                               content='',
                               theory_id=analysis_input.theory_id,
                               theory_name='')


@router.post("/output_mix_theory_report")
async def output_mix_theory_report(analysis_input: MixTheoryInputType,
                                   background_tasks: BackgroundTasks) -> MixTheoryRespType:
    background_tasks.add_task(stream_mix_theory_report, analysis_input)

    return MixTheoryRespType(id=analysis_input.session_id,
                             content='',
                             theory_name=[],
                             theory_id=analysis_input.theory_id)

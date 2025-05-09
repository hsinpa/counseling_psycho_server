from fastapi import APIRouter, BackgroundTasks, HTTPException
from src.feature.llm_model import classic_llm_loader
from src.feature.supervisor.database.supervisor_db_ops import SupervisorReportDBOps
from src.feature.supervisor.database.transcript_db_ops import TranscriptDBOps
from src.feature.supervisor.supervisor_model import SupervisorAnalysisRespModel
from src.feature.supervisor.supervisor_utility import (
    transcript_segment_to_text,
)
from src.model.supervisor_model import TranscriptData, AnalyzeSpeechToReportInputModel
from src.repository.supervisor_repo import SupervisorRepo
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.service.streaming.sse_manager import get_sse
from src.utility.static_text import DB_TRANSCRIPT_STATUS_COMPLETE

router = APIRouter(prefix="/api/supervisor", tags=["Supervisor"])

@router.get("/get_speech_to_report/{session_id}")
async def get_speech_to_report(session_id: str):
    postgres_client = PostgreSQLClient()
    supervisor_report_db = SupervisorReportDBOps(postgres_client)

    report = await supervisor_report_db.db_ops_get_supervisor_report(session_id)

    if report is None:
        raise HTTPException(status_code=404, detail=f"report from {session_id} do not exist")

    return report

@router.post("/analyze_speech_to_report")
async def analyze_speech_to_report(p_input: AnalyzeSpeechToReportInputModel) -> SupervisorAnalysisRespModel:
    postgres_client = PostgreSQLClient()
    supervisor_report_db = SupervisorReportDBOps(postgres_client)
    transcript_db = TranscriptDBOps(postgres_client)

    full_text = transcript_segment_to_text(p_input.segments)
    transcript_data = await transcript_db.db_ops_get_transcript_info(p_input.session_id)

    await transcript_db.db_ops_update_transcript_info(p_input.session_id,
                                                TranscriptData(full_text=full_text, segments=p_input.segments),
                                                status=DB_TRANSCRIPT_STATUS_COMPLETE)

    supervisor_repo = SupervisorRepo(llm_loader=classic_llm_loader)
    repo_result = await supervisor_repo.generate_analysis_report(full_text)

    await supervisor_report_db.db_ops_insert_supervisor_report(
        transcript_id=transcript_data.id,
        analysis_data=repo_result
    )

    print(repo_result.model_dump_json())
    await get_sse().queue_message(p_input.socket_id, repo_result.model_dump_json())

    return repo_result


@router.post("/async_analyze_speech_to_report")
async def async_analyze_speech_to_report(p_input: AnalyzeSpeechToReportInputModel, background_tasks: BackgroundTasks):
    background_tasks.add_task(analyze_speech_to_report, p_input)
    return {'session_id': p_input.session_id, 'socket_id': p_input.socket_id}

@router.post("/manual_trigger_supervisor_analysis")
async def manual_analyze_speech_to_report() -> SupervisorAnalysisRespModel:
    supervisor_report_db = SupervisorReportDBOps(PostgreSQLClient())

    with open("./assets/text/mock/mock_conversation_1.txt", encoding='utf-8') as f:
        mock_data: str = f.read()

    supervisor_repo = SupervisorRepo(llm_loader=classic_llm_loader)
    repo_result = await supervisor_repo.generate_analysis_report(mock_data)

    await supervisor_report_db.db_ops_insert_supervisor_report(
        session_id='test_session',
        analysis_data=repo_result
    )

    return repo_result

import json
from fastapi.responses import StreamingResponse

from fastapi import APIRouter, BackgroundTasks, HTTPException
from src.feature.llm_model import classic_llm_loader
from src.feature.supervisor.database.supervisor_db_ops import SupervisorReportDBOps
from src.feature.supervisor.database.transcript_db_ops import TranscriptDBOps
from src.feature.supervisor.docx.docx_exporter import SupervisorDocxExporter
from src.feature.supervisor.supervisor_model import SupervisorAnalysisRespModel
from src.feature.supervisor.supervisor_utility import (
    transcript_segment_to_text,
)
from src.model.supervisor_model import TranscriptData, AnalyzeSpeechToReportInputModel, RetrieveSpeechToTextInputModel
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


@router.post("/manual_trigger_supervisor_analysis",
         response_class=StreamingResponse,          # OpenAPI metadata
         responses={200: {"content": {
             "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}
         }}})
async def export_analyze_speech_to_report(p_input: RetrieveSpeechToTextInputModel) -> StreamingResponse:
    report = await get_speech_to_report(p_input.session_id)

    analysis_resp = SupervisorAnalysisRespModel(
        case_conceptualization=report["case_conceptualization"],
        homework_assignment=report["homework_assignment"],
        issue_treatment_strategies=report["issue_treatment_strategies"],
    )

    supervisor_docx_exporter = SupervisorDocxExporter()
    buffer = supervisor_docx_exporter.export(analysis_resp)

    headers = {
        "Content-Disposition": 'attachment; filename="report.docx"'
    }

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )


@router.post("/manual_trigger_supervisor_analysis",
         response_class=StreamingResponse,          # OpenAPI metadata
         responses={200: {"content": {
             "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}
         }}})
async def manual_analyze_speech_to_report() -> StreamingResponse:
    with open("./assets/text/mock/mock_analysis_1.json", encoding='utf-8') as f:
        mock_data: str = f.read()

    supervisorDocxExporter = SupervisorDocxExporter()
    json_object = json.loads(mock_data)

    supervisor_repo = SupervisorRepo(llm_loader=classic_llm_loader)

    homework = supervisor_repo._post_process_homework(json_object)
    case_conceptualization = supervisor_repo._post_process_case_conceptualization(json_object)
    treatments = supervisor_repo._post_issue_treament_strategy(json_object)

    analysis_resp = SupervisorAnalysisRespModel(
        case_conceptualization=case_conceptualization,
        homework_assignment=homework,
        issue_treatment_strategies=treatments,
    )

    buffer = supervisorDocxExporter.export(analysis_resp)

    headers = {
        "Content-Disposition": 'attachment; filename="report.docx"'
    }

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )

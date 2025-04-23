import asyncio
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from src.llm_agents.llm_model import classic_llm_loader
from src.llm_agents.supervisor.database.supervisor_db_ops import SupervisorReportDBOps
from src.llm_agents.supervisor.database.transcript_db_ops import TranscriptDBOps
from src.llm_agents.supervisor.supervisor_model import SupervisorAnalysisRespModel
from src.llm_agents.supervisor.supervisor_utility import transcript_segment_to_text
from src.model.supervisor_model import SpeechToTextLangEnum, RetrieveSpeechToTextInputModel, TranscribeStatus, \
    TranscriptData, TranscribeProgressEnum, AnalyzeSpeechToReportInputModel, TranscriptSegment
from src.repository.supervisor_repo import SupervisorRepo
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.service.speech_to_text.boto_helper import BotoHelper
from src.service.streaming.sse_manager import get_sse
from src.utility.static_text import DB_TRANSCRIPT_STATUS_COMPLETE, DB_TRANSCRIPT_STATUS_IN_PROGRESS

router = APIRouter(prefix="/api/supervisor", tags=["Supervisor"])

@router.post("/upload_speech_to_text")
async def upload_speech_to_text(
    audio_file: UploadFile = File(...),
    langcode: SpeechToTextLangEnum = Form(...),
    user_id: str = Form(...),
    session_id: str = Form(...)
):

    transcript_db = TranscriptDBOps(PostgreSQLClient())
    await transcript_db.db_ops_insert_transcript_info(session_id, user_id, audio_file.filename,
                                                      TranscriptData(full_text='', segments=[]))

    file_content = await audio_file.read()

    s3_bucket = 'audio-disk'
    s3_key = f'{session_id}-{audio_file.filename}'

    boto_helper = BotoHelper()

    s3_url = await asyncio.to_thread(boto_helper.upload_to_s3, audio_file,  file_content, s3_bucket, s3_key)
    transcribe_response = await asyncio.to_thread(boto_helper.request_transcribe, session_id, langcode, s3_bucket, s3_key)

    # print('transcribe_response', transcribe_response)

    return {'s3_bucket': s3_bucket, 's3_key': s3_key}


@router.get("/retrieve_speech_to_text_list/{user_id}")
async def retrieve_speech_to_text_list(user_id: str):
    transcript_db = TranscriptDBOps(PostgreSQLClient())
    return await transcript_db.db_ops_get_transcript_list(user_id)

@router.get("/retrieve_speech_to_text/{session_id}")
async def retrieve_speech_to_text(session_id: str) -> TranscribeStatus:
    # Retrieve from DB
    transcript_db = TranscriptDBOps(PostgreSQLClient())
    db_result = await transcript_db.db_ops_get_transcript_info(session_id)

    if db_result is not None and db_result.status == DB_TRANSCRIPT_STATUS_COMPLETE:
        return TranscribeStatus(status=TranscribeProgressEnum.complete, transcript_data=TranscriptData(
            full_text=db_result.full_text,
            segments=db_result.segments,
        ))

    # Query AWS Transcribe
    try:
        boto_helper = BotoHelper()
        status, transcript_uri  = await asyncio.to_thread(boto_helper.get_transcribe_status, session_id)

        if status == TranscribeProgressEnum.complete and transcript_uri is not None:
            transcript_data: TranscriptData = await asyncio.to_thread(boto_helper.retrieve_transcribe,
                                                                      transcript_uri)

            await transcript_db.db_ops_update_transcript_info(session_id, transcript_data, DB_TRANSCRIPT_STATUS_COMPLETE)

            return TranscribeStatus(status=status, transcript_data=transcript_data)

        return TranscribeStatus(status=status)
    except Exception as e:
        print(f'retrieve_speech_to_text session {session_id} fail', e)
        return TranscribeStatus(status=TranscribeProgressEnum.fail)

@router.post("/analyze_speech_to_report")
async def analyze_speech_to_report(p_input: AnalyzeSpeechToReportInputModel) -> SupervisorAnalysisRespModel:
    postgres_client = PostgreSQLClient()
    supervisor_report_db = SupervisorReportDBOps(postgres_client)
    transcript_db = TranscriptDBOps(postgres_client)

    full_text = transcript_segment_to_text(p_input.segments)
    await transcript_db.db_ops_update_transcript_info(p_input.session_id,
                                                TranscriptData(full_text=full_text, segments=p_input.segments))

    supervisor_repo = SupervisorRepo(llm_loader=classic_llm_loader)
    repo_result = await supervisor_repo.generate_analysis_report(full_text)

    await supervisor_report_db.db_ops_insert_supervisor_report(
        session_id=p_input.session_id,
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

import asyncio
from http.client import HTTPException

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import TypeAdapter

from src.llm_agents.llm_model import classic_llm_loader
from src.llm_agents.supervisor.database.transcript_db_ops import TranscriptDBOps
from src.llm_agents.supervisor.supervisor_model import SupervisorAnalysisRespModel
from src.model.supervisor_model import SpeechToTextLangEnum, RetrieveSpeechToTextInputModel, TranscribeStatus, \
    TranscriptData, TranscribeProgressEnum, AnalyzeSpeechToReportInputModel, TranscriptSegment
from src.repository.supervisor_repo import SupervisorRepo
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.service.speech_to_text.boto_helper import BotoHelper

router = APIRouter(prefix="/api/supervisor", tags=["Supervisor"])

@router.post("/upload_speech_to_text")
async def upload_speech_to_text(
    audio_file: UploadFile = File(...),
    langcode: SpeechToTextLangEnum = Form(...),
    session_id: str = Form(...)
):
    print('Session', session_id)
    print('File name', audio_file.filename)

    file_content = await audio_file.read()

    s3_bucket = 'audio-disk'
    s3_key = f'{session_id}-{audio_file.filename}'

    boto_helper = BotoHelper()

    s3_url = await asyncio.to_thread(boto_helper.upload_to_s3, audio_file,  file_content, s3_bucket, s3_key)
    transcribe_response = await asyncio.to_thread(boto_helper.request_transcribe, session_id, langcode, s3_bucket, s3_key)

    # print('transcribe_response', transcribe_response)

    return {'s3_bucket': s3_bucket, 's3_key': s3_key}

@router.get("/retrieve_speech_to_text/{session_id}")
async def retrieve_speech_to_text(session_id: str) -> TranscribeStatus:
    # Retrieve from DB
    transcript_db = TranscriptDBOps(PostgreSQLClient())
    db_result = await transcript_db.db_ops_get_transcript_info(session_id)

    if db_result is not None:
        return TranscribeStatus(status=TranscribeProgressEnum.complete, transcript_data=db_result)

    # Query AWS Transcribe
    try:
        boto_helper = BotoHelper()
        status, transcript_uri  = await asyncio.to_thread(boto_helper.get_transcribe_status, session_id)

        if status == TranscribeProgressEnum.complete and transcript_uri is not None:
            transcript_data: TranscriptData = await asyncio.to_thread(boto_helper.retrieve_transcribe,
                                                                      transcript_uri)

            await transcript_db.db_ops_insert_transcript_info(session_id, transcript_data)
            return TranscribeStatus(status=status, transcript_data=transcript_data)

        return TranscribeStatus(status=status)
    except Exception as e:
        print(f'retrieve_speech_to_text session {session_id} fail', e)
        return TranscribeStatus(status=TranscribeProgressEnum.fail)

@router.post("/retrieve_speech_to_text")
async def analyze_speech_to_report(p_input: AnalyzeSpeechToReportInputModel) -> SupervisorAnalysisRespModel:
    with open("./assets/text/mock/mock_conversation_2.txt", encoding='utf-8') as f:
        mock_data: str = f.read()

    supervisor_repo = SupervisorRepo(llm_loader=classic_llm_loader)
    repo_result = await supervisor_repo.generate_analysis_report(mock_data)

    return repo_result
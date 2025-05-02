import asyncio
from fastapi import APIRouter, UploadFile, File, Form
from src.llm_agents.supervisor.database.transcript_db_ops import TranscriptDBOps
from src.llm_agents.supervisor.supervisor_utility import (
    text_to_transcript_segment,
)
from src.model.supervisor_model import SpeechToTextLangEnum, RetrieveSpeechToTextInputModel, TranscribeStatus, \
    TranscriptData, TranscribeProgressEnum
from src.service.relation_db.postgresql_db_client import PostgreSQLClient
from src.service.speech_to_text.boto_helper import BotoHelper
from src.utility.static_text import DB_TRANSCRIPT_STATUS_COMPLETE

router = APIRouter(prefix="/api/transcript", tags=["Transcript"])


@router.post("/upload_speech_to_text")
async def upload_speech_to_text(
    file: UploadFile = File(...),
    langcode: SpeechToTextLangEnum = Form(...),
    user_id: str = Form(...),
    session_id: str = Form(...)
):
    transcript_db = TranscriptDBOps(PostgreSQLClient())
    await transcript_db.db_ops_insert_transcript_info(session_id, user_id, file.filename, langcode,
                                                      TranscriptData(full_text='', segments=[]))

    file_content = await file.read()

    s3_bucket = 'audio-disk'
    s3_key = f'{session_id}-{file.filename}'

    boto_helper = BotoHelper()

    s3_url = await asyncio.to_thread(boto_helper.upload_to_s3, file,  file_content, s3_bucket, s3_key)
    transcribe_response = await asyncio.to_thread(boto_helper.request_transcribe, session_id, langcode, s3_bucket, s3_key)

    return {'s3_bucket': s3_bucket, 's3_key': s3_key}

@router.post("/upload_txt_to_text")
async def upload_txt_to_text(
    file: UploadFile = File(...),
    langcode: SpeechToTextLangEnum = Form(...),
    user_id: str = Form(...),
    session_id: str = Form(...)
):
    transcript_db = TranscriptDBOps(PostgreSQLClient())

    # Read the file content
    content = await file.read()

    # Decode bytes to string
    text_content = content.decode("utf-8")

    parsed_segments = text_to_transcript_segment(text_content)

    await transcript_db.db_ops_insert_transcript_info(session_id, user_id, file.filename, langcode,
                                                      TranscriptData(full_text='', segments=parsed_segments),
                                                      DB_TRANSCRIPT_STATUS_COMPLETE)

    return {}


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

@router.delete("/delete_transcript")
async def delete_transcript(param_input: RetrieveSpeechToTextInputModel):
    transcript_db = TranscriptDBOps(PostgreSQLClient())
    transcript_type = await transcript_db.db_ops_get_transcript_info(param_input.session_id)

    if transcript_type is not None:
        await transcript_db.db_ops_delete_transcript(transcript_type.id)

    return {}

@router.put("/update_transcript_name")
async def update_transcript_name(file_name: str, session_id: str):
    transcript_db = TranscriptDBOps(PostgreSQLClient())
    await transcript_db.db_ops_update_transcript_name(file_name=file_name, session_id=session_id)

    return {}

import asyncio
from fastapi import APIRouter, UploadFile, File, Form

from src.model.supervisor_model import SpeechToTextLangEnum, RetrieveSpeechToTextInputModel, TranscribeStatus, \
    TranscriptData, TranscribeProgressEnum
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
    boto_helper = BotoHelper()

    status, transcript_uri  = await asyncio.to_thread(boto_helper.get_transcribe_status, session_id)

    if status == TranscribeProgressEnum.complete and transcript_uri is not None:
        transcript_data: TranscriptData = await asyncio.to_thread(boto_helper.retrieve_transcribe,
                                                                  transcript_uri)

        return TranscribeStatus(status=status, transcript_data=transcript_data)

    return TranscribeStatus(status=status)

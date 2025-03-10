import asyncio
from fastapi import APIRouter, UploadFile, File, Form

from src.service.speech_to_text.boto_helper import BotoHelper

router = APIRouter(prefix="/api/supervisor", tags=["Supervisor"])

@router.post("/upload_speech_to_text")
async def chat(
    audio_file: UploadFile = File(...),
    session_id: str = Form(...)
):
    print('Session', session_id)
    print('File name', audio_file.filename)

    file_content = await audio_file.read()

    s3_bucket = 'audio-disk'
    s3_key = f'{session_id}-{audio_file.filename}'

    boto_helper = BotoHelper()

    s3_url = await asyncio.to_thread(boto_helper.upload_to_s3, audio_file,  file_content, s3_bucket, s3_key)

    return {'s3_bucket': s3_bucket, 's3_key': s3_key}


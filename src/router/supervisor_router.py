import os
import shutil

from fastapi import APIRouter
from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter(prefix="/api/supervisor", tags=["Supervisor"])

@router.post("/upload_speech_to_text")
async def chat(
    audio_file: UploadFile = File(...),
    session_id: str = Form(...)
):
    print('Session', session_id)
    print('File name', audio_file.filename)

    return {'output': 'output'}


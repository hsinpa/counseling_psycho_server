from pydantic import BaseModel
from fastapi import UploadFile


class UploadSpeechToTextInputModel(BaseModel):
    audio_file: UploadFile
    session_id: str
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from fastapi import UploadFile

class SpeechToTextLangEnum(str, Enum):
    en_us = "en-US",
    zh_tw = "zh-TW",

class TranscribeProgressEnum(str, Enum):
    in_progress = "IN_PROGRESS",
    in_analyze = "IN_ANALYZE",
    complete = "COMPLETED",
    fail = "FAILED",

class TranscriptSegment(BaseModel):
    id: str
    speaker: str
    start_time: str
    end_time: str
    text: str

class TranscriptData(BaseModel):
    full_text: str
    segments: list[TranscriptSegment]

class TranscribeStatus(BaseModel):
    status: TranscribeProgressEnum
    transcript_data: Optional[TranscriptData] = None

# region API
class RetrieveSpeechToTextInputModel(BaseModel):
    session_id: str

class AnalyzeSpeechToReportInputModel(BaseModel):
    segments: list[TranscriptSegment]
    session_id: str
    socket_id: Optional[str] = Field('', description='ID For Socket')
# endregion
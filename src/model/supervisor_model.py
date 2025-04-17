from enum import Enum
from typing import Optional

from pydantic import BaseModel
from fastapi import UploadFile

class SpeechToTextLangEnum(str, Enum):
    en_us: str = "en-US",
    zh_tw: str = "zh-TW",

class TranscribeProgressEnum(str, Enum):
    in_progress: str = "IN_PROGRESS",
    complete: str = "COMPLETED",
    fail: str = "FAILED",


class TranscriptSegment(BaseModel):
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
    speech_text: str
    session_id: str
# endregion
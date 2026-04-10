# app/schemas/voice.py
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class VoiceSessionStart(BaseModel):
    period: str


class VoiceTranscription(BaseModel):
    question_index: int
    transcription: str


class VoiceSessionSubmit(BaseModel):
    period: str
    transcriptions: List[VoiceTranscription]


class VoiceQuestion(BaseModel):
    index: int
    text: str
    audio_url: Optional[str] = None


class VoiceSessionResponse(BaseModel):
    session_id: str
    questions: List[VoiceQuestion]
    first_audio_base64: str


class VoiceAnalysisResponse(BaseModel):
    analysis: str
    mood_score: int
    sleep_hours: Optional[float] = None
    recommendations: List[str]
    saved_checkin_id: UUID
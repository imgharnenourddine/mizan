# app/api/v1/routes/voice.py
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.voice import (
    VoiceAnalysisResponse,
    VoiceSessionResponse,
    VoiceSessionStart,
    VoiceSessionSubmit,
)
from app.services.student_service import get_student_by_user_id
from app.services.voice_service import (
    analyze_voice_responses,
    start_voice_session,
    transcribe_audio,
)

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/start", response_model=VoiceSessionResponse)
async def api_start_voice_session(
    data: VoiceSessionStart,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    return await start_voice_session(db, student.id, data.period)


@router.post("/transcribe")
async def api_transcribe_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    text = await transcribe_audio(file)
    return {"transcription": text}


@router.post("/submit", response_model=VoiceAnalysisResponse)
async def api_submit_voice_session(
    data: VoiceSessionSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    return await analyze_voice_responses(db, student.id, data)
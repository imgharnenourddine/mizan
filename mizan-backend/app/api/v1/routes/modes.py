# Work mode tracking endpoints — start/stop mode session, get current mode, weekly stats
# app/api/v1/routes/modes.py
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.mode import ModeSessionCreate, ModeSessionResponse, ModeStatsResponse
from app.services.mode_service import (
    get_current_mode,
    get_mode_stats,
    start_mode,
    stop_current_mode,
)
from app.services.student_service import get_student_by_user_id

router = APIRouter(prefix="/modes", tags=["Modes"])


@router.post("/start", response_model=ModeSessionResponse)
async def api_start_mode(
    data: ModeSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    return await start_mode(db, student.id, data)


@router.post("/stop", response_model=ModeSessionResponse)
async def api_stop_mode(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    return await stop_current_mode(db, student.id)


@router.get("/current", response_model=Optional[ModeSessionResponse])
async def api_get_current_mode(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    return await get_current_mode(db, student.id)


@router.get("/stats", response_model=ModeStatsResponse)
async def api_get_mode_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    return await get_mode_stats(db, student.id)
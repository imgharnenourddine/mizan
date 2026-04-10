# Work mode session tracker — start/stop sessions, compute weekly mode distribution
# app/services/mode_service.py
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mode_session import Mode, ModeSession
from app.schemas.mode import ModeSessionCreate, ModeStatItem, ModeStatsResponse


async def start_mode(db: AsyncSession, student_id: UUID, data: ModeSessionCreate) -> ModeSession:
    now = datetime.now(timezone.utc)
    
    result = await db.execute(
        select(ModeSession).where(
            and_(ModeSession.student_id == student_id, ModeSession.ended_at.is_(None))
        )
    )
    active_session = result.scalars().first()
    
    if active_session:
        active_session.ended_at = now
        duration = int((now - active_session.started_at).total_seconds() / 60)
        active_session.duration_minutes = duration
        
    new_session = ModeSession(
        student_id=student_id,
        mode=data.mode,
        started_at=now,
        ended_at=None,
        duration_minutes=None
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


async def stop_current_mode(db: AsyncSession, student_id: UUID) -> ModeSession:
    now = datetime.now(timezone.utc)
    
    result = await db.execute(
        select(ModeSession).where(
            and_(ModeSession.student_id == student_id, ModeSession.ended_at.is_(None))
        )
    )
    active_session = result.scalars().first()
    
    if not active_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active mode session found"
        )
        
    active_session.ended_at = now
    duration = int((now - active_session.started_at).total_seconds() / 60)
    active_session.duration_minutes = duration
    
    await db.commit()
    await db.refresh(active_session)
    return active_session


async def get_current_mode(db: AsyncSession, student_id: UUID) -> ModeSession | None:
    result = await db.execute(
        select(ModeSession).where(
            and_(ModeSession.student_id == student_id, ModeSession.ended_at.is_(None))
        )
    )
    return result.scalars().first()


async def get_mode_stats(db: AsyncSession, student_id: UUID) -> ModeStatsResponse:
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())

    result = await db.execute(
        select(ModeSession).where(
            and_(ModeSession.student_id == student_id, ModeSession.started_at >= week_start)
        )
    )
    sessions = result.scalars().all()

    today_totals = {m: 0 for m in Mode}
    week_totals = {m: 0 for m in Mode}
    current_session = None

    for session in sessions:
        if session.ended_at is None:
            current_session = session
            duration = int((now - session.started_at).total_seconds() / 60)
        else:
            duration = session.duration_minutes or 0

        week_totals[session.mode] += duration
        
        if session.started_at >= today_start:
            today_totals[session.mode] += duration

    today_stats = [ModeStatItem(mode=k, total_minutes=v) for k, v in today_totals.items() if v > 0]
    week_stats = [ModeStatItem(mode=k, total_minutes=v) for k, v in week_totals.items() if v > 0]

    return ModeStatsResponse(
        today=today_stats,
        this_week=week_stats,
        current_session=current_session
    )
# Morning and evening check-in business logic — save responses, build briefing, query history
# app/services/checkin_service.py
from datetime import date, timedelta
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.checkin import EveningCheckin, MorningCheckin
from app.models.student import Exam, Project, Schedule
from app.schemas.checkin import EveningCheckinCreate, MorningCheckinCreate
from app.services.agent_service import generate_daily_plan


async def get_morning_briefing(db: AsyncSession, student_id: UUID) -> dict:
    today = date.today()
    day_name = today.strftime("%A")
    three_days_later = today + timedelta(days=3)
    five_days_later = today + timedelta(days=5)

    schedule_res = await db.execute(
        select(Schedule).where(and_(Schedule.student_id == student_id, Schedule.day_of_week == day_name))
    )
    schedules = schedule_res.scalars().all()

    exam_res = await db.execute(
        select(Exam).where(and_(Exam.student_id == student_id, Exam.exam_date >= today, Exam.exam_date <= three_days_later))
    )
    exams = exam_res.scalars().all()

    project_res = await db.execute(
        select(Project).where(and_(Project.student_id == student_id, Project.due_date >= today, Project.due_date <= five_days_later))
    )
    projects = project_res.scalars().all()

    evening_res = await db.execute(
        select(EveningCheckin)
        .where(EveningCheckin.student_id == student_id)
        .order_by(desc(EveningCheckin.date))
        .limit(1)
    )
    last_evening = evening_res.scalars().first()
    last_evening_mood = last_evening.mood_score if last_evening else None

    return {
        "today_schedule": schedules,
        "upcoming_exams": exams,
        "upcoming_projects": projects,
        "last_evening_mood": last_evening_mood
    }


async def has_morning_checkin_today(db: AsyncSession, student_id: UUID) -> bool:
    today = date.today()
    res = await db.execute(
        select(MorningCheckin).where(and_(MorningCheckin.student_id == student_id, MorningCheckin.date == today))
    )
    return res.scalars().first() is not None


async def has_evening_checkin_today(db: AsyncSession, student_id: UUID) -> bool:
    today = date.today()
    res = await db.execute(
        select(EveningCheckin).where(and_(EveningCheckin.student_id == student_id, EveningCheckin.date == today))
    )
    return res.scalars().first() is not None


async def create_morning_checkin(db: AsyncSession, student_id: UUID, data: MorningCheckinCreate) -> MorningCheckin:
    if await has_morning_checkin_today(db, student_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already checked in this morning.")

    context = await get_morning_briefing(db, student_id)
    generated_plan = await generate_daily_plan(context, data.sleep_hours, data.mood_score)

    checkin = MorningCheckin(
        student_id=student_id,
        date=date.today(),
        sleep_hours=data.sleep_hours,
        mood_score=data.mood_score,
        generated_plan=generated_plan
    )
    db.add(checkin)
    await db.commit()
    await db.refresh(checkin)
    return checkin


async def create_evening_checkin(db: AsyncSession, student_id: UUID, data: EveningCheckinCreate) -> EveningCheckin:
    if await has_evening_checkin_today(db, student_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already checked in this evening.")

    checkin = EveningCheckin(
        student_id=student_id,
        date=date.today(),
        plan_completed=data.plan_completed,
        mood_score=data.mood_score,
        notes=data.notes
    )
    db.add(checkin)
    await db.commit()
    await db.refresh(checkin)
    return checkin


async def get_checkin_history(db: AsyncSession, student_id: UUID, days: int = 7) -> dict:
    start_date = date.today() - timedelta(days=days)

    morning_res = await db.execute(
        select(MorningCheckin)
        .where(and_(MorningCheckin.student_id == student_id, MorningCheckin.date >= start_date))
        .order_by(MorningCheckin.date)
    )
    morning_checkins = list(morning_res.scalars().all())

    evening_res = await db.execute(
        select(EveningCheckin)
        .where(and_(EveningCheckin.student_id == student_id, EveningCheckin.date >= start_date))
        .order_by(EveningCheckin.date)
    )
    evening_checkins = list(evening_res.scalars().all())

    avg_morning_mood = sum(c.mood_score for c in morning_checkins) / len(morning_checkins) if morning_checkins else 0
    avg_evening_mood = sum(c.mood_score for c in evening_checkins) / len(evening_checkins) if evening_checkins else 0
    avg_sleep = sum(c.sleep_hours for c in morning_checkins) / len(morning_checkins) if morning_checkins else 0

    return {
        "morning_checkins": morning_checkins,
        "evening_checkins": evening_checkins,
        "averages": {
            "morning_mood": round(avg_morning_mood, 2),
            "evening_mood": round(avg_evening_mood, 2),
            "sleep_hours": round(avg_sleep, 2)
        }
    }
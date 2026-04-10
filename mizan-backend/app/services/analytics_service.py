# Analytics computations — mood patterns, sleep averages, stress detection, weekly stats
# app/services/analytics_service.py
from datetime import date, datetime, timedelta, timezone
from typing import List
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.checkin import EveningCheckin, MorningCheckin
from app.models.goal import Goal, GoalProgress
from app.models.mode_session import ModeSession
from app.models.student import Exam, Schedule, Student
from app.schemas.analytics import (
    ModeDistribution,
    MoodGraphPoint,
    StudentDashboard,
    WeeklyReport,
)
from app.services.checkin_service import (
    has_evening_checkin_today,
    has_morning_checkin_today,
)
from app.services.mode_service import get_current_mode


async def get_mood_graph(db: AsyncSession, student_id: UUID, days: int = 30) -> List[MoodGraphPoint]:
    start_date = date.today() - timedelta(days=days)
    
    result = await db.execute(
        select(MorningCheckin)
        .where(and_(MorningCheckin.student_id == student_id, MorningCheckin.date >= start_date))
        .order_by(MorningCheckin.date)
    )
    checkins = result.scalars().all()
    
    return [
        MoodGraphPoint(date=c.date, mood_score=float(c.mood_score), sleep_hours=c.sleep_hours)
        for c in checkins
    ]


async def get_mode_distribution(db: AsyncSession, student_id: UUID, days: int = 7) -> List[ModeDistribution]:
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)
    
    result = await db.execute(
        select(ModeSession).where(
            and_(ModeSession.student_id == student_id, ModeSession.started_at >= start_date)
        )
    )
    sessions = result.scalars().all()
    
    totals = {}
    for s in sessions:
        if s.ended_at is None:
            duration = int((now - s.started_at).total_seconds() / 60)
        else:
            duration = s.duration_minutes or 0
            
        mode_str = s.mode.value if hasattr(s.mode, 'value') else str(s.mode)
        totals[mode_str] = totals.get(mode_str, 0) + duration
        
    total_time = sum(totals.values())
    
    distribution = []
    for mode, duration in totals.items():
        if duration > 0:
            percentage = round((duration / total_time * 100), 2) if total_time > 0 else 0.0
            distribution.append(ModeDistribution(mode=mode, total_minutes=duration, percentage=percentage))
            
    return distribution


async def get_weekly_report(db: AsyncSession, student_id: UUID) -> WeeklyReport:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    morning_res = await db.execute(
        select(MorningCheckin).where(
            and_(MorningCheckin.student_id == student_id, MorningCheckin.date >= week_start, MorningCheckin.date <= week_end)
        )
    )
    mornings = morning_res.scalars().all()
    
    evening_res = await db.execute(
        select(EveningCheckin).where(
            and_(EveningCheckin.student_id == student_id, EveningCheckin.date >= week_start, EveningCheckin.date <= week_end)
        )
    )
    evenings = evening_res.scalars().all()
    
    total_checkins = len(mornings) + len(evenings)
    
    avg_mood = 0.0
    all_moods = [m.mood_score for m in mornings] + [e.mood_score for e in evenings]
    if all_moods:
        avg_mood = sum(all_moods) / len(all_moods)
        
    avg_sleep = 0.0
    if mornings:
        avg_sleep = sum(m.sleep_hours for m in mornings) / len(mornings)
        
    stress_level = "LOW"
    if avg_mood <= 2.0 and len(all_moods) > 0:
        stress_level = "HIGH"
    elif avg_mood <= 3.5 and len(all_moods) > 0:
        stress_level = "MEDIUM"
        
    goals_res = await db.execute(select(Goal).where(Goal.student_id == student_id, Goal.is_active == True))
    goals = goals_res.scalars().all()
    
    prog_res = await db.execute(
        select(GoalProgress).where(
            and_(GoalProgress.date >= week_start, GoalProgress.date <= week_end)
        )
    )
    progresses = prog_res.scalars().all()
    
    prog_map = {}
    for p in progresses:
        prog_map[p.goal_id] = prog_map.get(p.goal_id, 0.0) + p.value
        
    goals_achieved = sum(1 for g in goals if prog_map.get(g.id, 0.0) >= g.target_value)
    
    mode_distribution = await get_mode_distribution(db, student_id, days=7)
    
    return WeeklyReport(
        week_start=week_start,
        week_end=week_end,
        avg_mood=round(avg_mood, 2),
        avg_sleep=round(avg_sleep, 2),
        total_checkins=total_checkins,
        goals_achieved=goals_achieved,
        mode_distribution=mode_distribution,
        stress_level=stress_level
    )


async def get_student_dashboard(db: AsyncSession, student_id: UUID) -> StudentDashboard:
    today = date.today()
    day_name = today.strftime("%A")
    three_days_later = today + timedelta(days=3)
    
    student_res = await db.execute(select(Student).where(Student.id == student_id))
    student = student_res.scalars().first()
    
    current_mode = await get_current_mode(db, student_id)
    has_morning = await has_morning_checkin_today(db, student_id)
    has_evening = await has_evening_checkin_today(db, student_id)
    
    goals_res = await db.execute(
        select(func.count()).select_from(Goal).where(Goal.student_id == student_id, Goal.is_active == True)
    )
    active_goals_count = goals_res.scalar() or 0
    
    exam_res = await db.execute(
        select(Exam).where(and_(Exam.student_id == student_id, Exam.exam_date >= today, Exam.exam_date <= three_days_later))
    )
    upcoming_exams = list(exam_res.scalars().all())
    
    sched_res = await db.execute(
        select(Schedule).where(and_(Schedule.student_id == student_id, Schedule.day_of_week == day_name))
    )
    today_schedule = list(sched_res.scalars().all())
    
    mood_trend = await get_mood_graph(db, student_id, days=7)
    
    return StudentDashboard(
        student=student,
        current_mode=current_mode,
        has_morning_checkin=has_morning,
        has_evening_checkin=has_evening,
        active_goals_count=active_goals_count,
        upcoming_exams=upcoming_exams,
        today_schedule=today_schedule,
        mood_trend=mood_trend
    )
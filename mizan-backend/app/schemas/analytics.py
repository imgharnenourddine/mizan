# Pydantic schemas for analytics — WeeklyReport, MoodGraph, SleepGraph, ModeDistribution
# app/schemas/analytics.py
from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.mode import ModeSessionResponse
from app.schemas.student import ExamResponse, ScheduleResponse, StudentResponse


class MoodGraphPoint(BaseModel):
    date: date
    mood_score: float
    sleep_hours: float


class ModeDistribution(BaseModel):
    mode: str
    total_minutes: int
    percentage: float


class WeeklyReport(BaseModel):
    week_start: date
    week_end: date
    avg_mood: float
    avg_sleep: float
    total_checkins: int
    goals_achieved: int
    mode_distribution: List[ModeDistribution]
    stress_level: str


class StudentDashboard(BaseModel):
    student: StudentResponse
    current_mode: Optional[ModeSessionResponse] = None
    has_morning_checkin: bool
    has_evening_checkin: bool
    active_goals_count: int
    upcoming_exams: List[ExamResponse]
    today_schedule: List[ScheduleResponse]
    mood_trend: List[MoodGraphPoint]
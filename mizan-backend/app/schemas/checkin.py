# Pydantic schemas for check-ins — MorningCheckinCreate, EveningCheckinCreate, PlanResponse
# app/schemas/checkin.py
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MorningCheckinCreate(BaseModel):
    sleep_hours: float
    mood_score: int = Field(ge=1, le=5)


class EveningCheckinCreate(BaseModel):
    plan_completed: bool
    mood_score: int = Field(ge=1, le=5)
    notes: Optional[str] = None


class MorningCheckinResponse(BaseModel):
    id: UUID
    student_id: UUID
    date: date
    sleep_hours: float
    mood_score: int
    generated_plan: str
    checkin_time: datetime

    model_config = ConfigDict(from_attributes=True)


class EveningCheckinResponse(BaseModel):
    id: UUID
    student_id: UUID
    date: date
    plan_completed: bool
    mood_score: int
    notes: Optional[str]
    checkin_time: datetime

    model_config = ConfigDict(from_attributes=True)
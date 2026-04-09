# SQLAlchemy ModeSession model — tracks work mode (revision, exam, project, rest, sport, class)
# app/models/mode_session.py
import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Mode(str, enum.Enum):
    REVISION = "REVISION"
    EXAMEN = "EXAMEN"
    PROJET = "PROJET"
    REPOS = "REPOS"
    SPORT = "SPORT"
    COURS = "COURS"


class ModeSession(Base):
    __tablename__ = "mode_session"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("student.id"), nullable=False)
    mode: Mapped[Mode] = mapped_column(String, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    student: Mapped["Student"] = relationship("Student", back_populates="mode_sessions")
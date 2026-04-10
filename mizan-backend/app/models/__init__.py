# Models package — imports all ORM models so Alembic can detect them for migrations


# app/models/__init__.py
from app.models.user import User, Role
from app.models.institution import School, Filiere, Promotion, Class
from app.models.student import Student, Schedule, Exam, Project
from app.models.checkin import MorningCheckin, EveningCheckin
from app.models.goal import Goal, GoalProgress
from app.models.mode_session import ModeSession, Mode
from app.models.resource import WellbeingResource, ResourceType
from app.models.voice_session import VoiceSession, VoiceSessionStatus

__all__ = [
    "User",
    "Role",
    "School",
    "Filiere",
    "Promotion",
    "Class",
    "Student",
    "Schedule",
    "Exam",
    "Project",
    "MorningCheckin",
    "EveningCheckin",
    "Goal",
    "GoalProgress",
    "ModeSession",
    "Mode",
    "WellbeingResource",
    "ResourceType",
    "VoiceSession",
    "VoiceSessionStatus"
]
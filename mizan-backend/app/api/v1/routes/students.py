# Student profile endpoints — list, detail, activation, schedule, exams
# app/api/v1/routes/students.py
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.student import StudentResponse
from app.services.student_service import (
    get_student_by_user_id,
    get_student_context,
    import_exams_from_csv,
    import_projects_from_csv,
    import_schedule_from_csv,
    import_students_from_csv,
)

router = APIRouter(prefix="/students", tags=["Students"])

from app.models.user import User, Role

admin_dep = Depends(require_role(Role.ADMIN))

@router.post("/import/trombi/{class_id}", dependencies=[admin_dep])
async def api_import_trombi(class_id: UUID, file: UploadFile, db: AsyncSession = Depends(get_db)):
    count = await import_students_from_csv(db, class_id, file)
    return {"message": f"Successfully imported {count} students"}

@router.post("/import/schedule/{class_id}", dependencies=[admin_dep])
async def api_import_schedule(class_id: UUID, file: UploadFile, db: AsyncSession = Depends(get_db)):
    count = await import_schedule_from_csv(db, class_id, file)
    return {"message": f"Successfully imported {count} schedule entries"}

@router.post("/import/exams/{class_id}", dependencies=[admin_dep])
async def api_import_exams(class_id: UUID, file: UploadFile, db: AsyncSession = Depends(get_db)):
    count = await import_exams_from_csv(db, class_id, file)
    return {"message": f"Successfully imported {count} exam entries"}

@router.post("/import/projects/{class_id}", dependencies=[admin_dep])
async def api_import_projects(class_id: UUID, file: UploadFile, db: AsyncSession = Depends(get_db)):
    count = await import_projects_from_csv(db, class_id, file)
    return {"message": f"Successfully imported {count} project entries"}
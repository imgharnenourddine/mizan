# app/api/v1/routes/files.py
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import Role
from app.models.student import Student
from app.services.file_service import (
    delete_photo_from_cloudinary,
    upload_photo_to_cloudinary,
    validate_image_file,
)
admin_dep = Depends(require_role(Role.ADMIN))
router = APIRouter(
    prefix="/files", 
    tags=["Files"],
    dependencies=[admin_dep]
)


@router.post("/students/{student_id}/photo")
async def api_upload_student_photo(
    student_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    validate_image_file(file)

    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    secure_url = await upload_photo_to_cloudinary(file, student.cne)
    
    student.photo_url = secure_url
    await db.commit()
    await db.refresh(student)

    return {"photo_url": secure_url}


@router.delete("/students/{student_id}/photo")
async def api_delete_student_photo(
    student_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if student.photo_url:
        await delete_photo_from_cloudinary(student.cne)
        student.photo_url = None
        await db.commit()

    return {"message": "Photo deleted"}
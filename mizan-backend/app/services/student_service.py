# Student profile management — activation, linking to class, trombinoscope CSV parsing
# app/services/student_service.py
from datetime import date, datetime, timedelta
from typing import Any, Dict
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.institution import Class
from app.models.mode_session import ModeSession
from app.models.student import Exam, Project, Schedule, Student
from app.models.user import Role, User
from app.utils.csv_parser import (
    parse_exam_csv,
    parse_project_csv,
    parse_schedule_csv,
    parse_trombi_csv,
)


async def _verify_class_exists(db: AsyncSession, class_id: UUID) -> None:
    result = await db.execute(select(Class).where(Class.id == class_id))
    if not result.scalars().first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")


async def import_students_from_csv(db: AsyncSession, class_id: UUID, file: UploadFile) -> int:
    await _verify_class_exists(db, class_id)
    rows = await parse_trombi_csv(file)
    count = 0
    
    for row in rows:
        email = row.get("email")
        if not email:
            continue
            
        user = User(email=email, role=Role.STUDENT, is_active=False)
        db.add(user)
        await db.flush()
        
        student = Student(
            user_id=user.id,
            class_id=class_id,
            first_name=row.get("prenom", ""),
            last_name=row.get("nom", ""),
            cne=row.get("cne", ""),
            phone=row.get("telephone"),
            photo_url=row.get("photo_url")
        )
        db.add(student)
        count += 1
        
    await db.commit()
    return count


async def import_schedule_from_csv(db: AsyncSession, class_id: UUID, file: UploadFile) -> int:
    await _verify_class_exists(db, class_id)
    rows = await parse_schedule_csv(file)
    
    student_result = await db.execute(select(Student.id).where(Student.class_id == class_id))
    student_ids = student_result.scalars().all()
    
    count = 0
    for row in rows:
        start_time_obj = datetime.strptime(row.get("start_time", "00:00"), "%H:%M").time()
        end_time_obj = datetime.strptime(row.get("end_time", "00:00"), "%H:%M").time()
        
        for s_id in student_ids:
            schedule = Schedule(
                student_id=s_id,
                subject=row.get("subject", ""),
                day_of_week=row.get("day_of_week", ""),
                start_time=start_time_obj,
                end_time=end_time_obj,
                room=row.get("room", ""),
                professor=row.get("professor", "")
            )
            db.add(schedule)
            count += 1
            
    await db.commit()
    return count


async def import_exams_from_csv(db: AsyncSession, class_id: UUID, file: UploadFile) -> int:
    await _verify_class_exists(db, class_id)
    rows = await parse_exam_csv(file)
    
    student_result = await db.execute(select(Student.id).where(Student.class_id == class_id))
    student_ids = student_result.scalars().all()
    
    count = 0
    for row in rows:
        exam_date_obj = datetime.strptime(row.get("exam_date", "2000-01-01"), "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(row.get("start_time", "00:00"), "%H:%M").time()
        end_time_obj = datetime.strptime(row.get("end_time", "00:00"), "%H:%M").time()
        
        for s_id in student_ids:
            exam = Exam(
                student_id=s_id,
                subject=row.get("subject", ""),
                exam_date=exam_date_obj,
                start_time=start_time_obj,
                end_time=end_time_obj,
                room=row.get("room", "")
            )
            db.add(exam)
            count += 1
            
    await db.commit()
    return count


async def import_projects_from_csv(db: AsyncSession, class_id: UUID, file: UploadFile) -> int:
    await _verify_class_exists(db, class_id)
    rows = await parse_project_csv(file)
    
    student_result = await db.execute(select(Student.id).where(Student.class_id == class_id))
    student_ids = student_result.scalars().all()
    
    count = 0
    for row in rows:
        due_date_obj = datetime.strptime(row.get("due_date", "2000-01-01"), "%Y-%m-%d").date()
        
        for s_id in student_ids:
            project = Project(
                student_id=s_id,
                name=row.get("name", ""),
                subject=row.get("subject", ""),
                due_date=due_date_obj,
                members=row.get("members", [])
            )
            db.add(project)
            count += 1
            
    await db.commit()
    return count


async def get_student_by_user_id(db: AsyncSession, user_id: UUID) -> Student:
    result = await db.execute(select(Student).where(Student.user_id == user_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    return student


async def get_student_context(db: AsyncSession, student_id: UUID) -> Dict[str, Any]:
    today = date.today()
    day_name = today.strftime("%A")
    upcoming_limit = today + timedelta(days=3)

    student_result = await db.execute(select(Student).where(Student.id == student_id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    schedule_result = await db.execute(
        select(Schedule).where(and_(Schedule.student_id == student_id, Schedule.day_of_week == day_name))
    )
    schedules = schedule_result.scalars().all()

    exam_result = await db.execute(
        select(Exam).where(and_(Exam.student_id == student_id, Exam.exam_date >= today, Exam.exam_date <= upcoming_limit))
    )
    exams = exam_result.scalars().all()

    project_result = await db.execute(
        select(Project).where(and_(Project.student_id == student_id, Project.due_date >= today))
    )
    projects = project_result.scalars().all()

    mode_result = await db.execute(
        select(ModeSession).where(and_(ModeSession.student_id == student_id, ModeSession.ended_at.is_(None)))
    )
    active_mode = mode_result.scalars().first()

    return {
        "student": student,
        "today_schedule": schedules,
        "upcoming_exams": exams,
        "active_projects": projects,
        "current_mode": active_mode
    }
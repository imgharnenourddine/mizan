# Personal goal tracking — create goals, record progress, detect completion and celebrate
# app/services/goal_service.py
from datetime import date
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.goal import Goal, GoalProgress
from app.schemas.goal import GoalCreate, GoalProgressCreate, GoalWithProgressResponse


async def create_goal(db: AsyncSession, student_id: UUID, data: GoalCreate) -> Goal:
    result = await db.execute(
        select(func.count()).select_from(Goal).where(Goal.student_id == student_id, Goal.is_active == True)
    )
    active_count = result.scalar() or 0

    if active_count >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 5 active goals allowed"
        )

    goal = Goal(
        student_id=student_id,
        title=data.title,
        target_value=data.target_value,
        unit=data.unit,
        is_active=True
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


async def get_student_goals(db: AsyncSession, student_id: UUID) -> List[Goal]:
    result = await db.execute(
        select(Goal).where(Goal.student_id == student_id, Goal.is_active == True)
    )
    return list(result.scalars().all())


async def get_goal_with_progress(db: AsyncSession, goal_id: UUID, student_id: UUID) -> GoalWithProgressResponse:
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.student_id == student_id)
    )
    goal = result.scalars().first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found or does not belong to the student"
        )

    progress_result = await db.execute(
        select(GoalProgress).where(GoalProgress.goal_id == goal_id).order_by(GoalProgress.date.desc())
    )
    progresses = list(progress_result.scalars().all())

    today = date.today()
    today_progress = sum(p.value for p in progresses if p.date == today)
    total_progress = sum(p.value for p in progresses)
    completion_percentage = (today_progress / goal.target_value * 100) if goal.target_value > 0 else 0.0

    return GoalWithProgressResponse(
        id=goal.id,
        student_id=goal.student_id,
        title=goal.title,
        target_value=goal.target_value,
        unit=goal.unit,
        is_active=goal.is_active,
        today_progress=today_progress,
        total_progress=total_progress,
        completion_percentage=completion_percentage,
        progress_history=progresses
    )


async def log_progress(db: AsyncSession, student_id: UUID, data: GoalProgressCreate) -> GoalProgress:
    result = await db.execute(
        select(Goal).where(Goal.id == data.goal_id, Goal.student_id == student_id)
    )
    goal = result.scalars().first()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    
    if not goal.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot log progress for an inactive goal"
        )

    progress = GoalProgress(
        goal_id=goal.id,
        date=date.today(),
        value=data.value,
        note=data.note
    )
    db.add(progress)
    await db.commit()
    await db.refresh(progress)
    return progress


async def deactivate_goal(db: AsyncSession, goal_id: UUID, student_id: UUID) -> Goal:
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.student_id == student_id)
    )
    goal = result.scalars().first()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found or does not belong to the student"
        )

    goal.is_active = False
    await db.commit()
    await db.refresh(goal)
    return goal


async def get_today_summary(db: AsyncSession, student_id: UUID) -> List[dict]:
    goals = await get_student_goals(db, student_id)
    if not goals:
        return []

    goal_ids = [g.id for g in goals]
    today = date.today()
    
    progress_result = await db.execute(
        select(GoalProgress).where(GoalProgress.goal_id.in_(goal_ids), GoalProgress.date == today)
    )
    today_progresses = progress_result.scalars().all()

    progress_map = {}
    for p in today_progresses:
        progress_map[p.goal_id] = progress_map.get(p.goal_id, 0.0) + p.value

    summary = []
    for goal in goals:
        today_val = progress_map.get(goal.id, 0.0)
        completion_percentage = (today_val / goal.target_value * 100) if goal.target_value > 0 else 0.0
        
        summary.append({
            "goal_id": goal.id,
            "title": goal.title,
            "target_value": goal.target_value,
            "unit": goal.unit,
            "today_value": today_val,
            "completion_percentage": completion_percentage,
            "achieved": today_val >= goal.target_value
        })

    return summary
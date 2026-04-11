# app/api/v1/routes/resources.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, Role
from app.models.checkin import MorningCheckin
from app.models.user import User
from app.schemas.resource import ResourceResponse
from app.services.resource_service import (
    get_all_resources,
    get_resources_for_mood,
    seed_default_resources,
)
from app.services.student_service import get_student_by_user_id

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/", response_model=List[ResourceResponse])
async def api_get_all_resources(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_resources(db)


@router.get("/for-me", response_model=List[ResourceResponse])
async def api_get_resources_for_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    
    result = await db.execute(
        select(MorningCheckin)
        .where(MorningCheckin.student_id == student.id)
        .order_by(desc(MorningCheckin.date))
        .limit(1)
    )
    last_checkin = result.scalars().first()
    
    mood_score = last_checkin.mood_score if last_checkin else 3
    
    return await get_resources_for_mood(db, mood_score)


@router.post("/seed", dependencies=[Depends(require_role(Role.ADMIN))])
async def api_seed_resources(db: AsyncSession = Depends(get_db)):
    await seed_default_resources(db)
    return {"message": "Resources seeded successfully"}
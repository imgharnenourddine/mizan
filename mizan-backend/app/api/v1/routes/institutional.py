from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, Role
from app.schemas.institution import (
    ClassCreate, ClassResponse,
    FiliereCreate, FiliereResponse,
    PromotionCreate, PromotionResponse,
    SchoolCreate, SchoolResponse,
)
from app.services.institutional_service import (
    create_class, create_filiere, create_promotion, create_school,
    get_all_schools, get_classes_by_promotion,
    get_filieres_by_school, get_promotions_by_filiere,
)

router = APIRouter(prefix="/institutional", tags=["Institutional"])

admin_dep = Depends(require_role(Role.ADMIN))

@router.post("/schools", response_model=SchoolResponse, dependencies=[admin_dep])
async def create_school_route(data: SchoolCreate, db: AsyncSession = Depends(get_db)):
    return await create_school(db, data)

@router.get("/schools", response_model=List[SchoolResponse], dependencies=[admin_dep])
async def api_get_all_schools(db: AsyncSession = Depends(get_db)):
    return await get_all_schools(db)

@router.post("/filieres", response_model=FiliereResponse, dependencies=[admin_dep])
async def api_create_filiere(data: FiliereCreate, db: AsyncSession = Depends(get_db)):
    return await create_filiere(db, data)

@router.get("/filieres/{school_id}", response_model=List[FiliereResponse], dependencies=[admin_dep])
async def api_get_filieres_by_school(school_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_filieres_by_school(db, school_id)

@router.post("/promotions", response_model=PromotionResponse, dependencies=[admin_dep])
async def api_create_promotion(data: PromotionCreate, db: AsyncSession = Depends(get_db)):
    return await create_promotion(db, data)

@router.get("/promotions/{filiere_id}", response_model=List[PromotionResponse], dependencies=[admin_dep])
async def api_get_promotions_by_filiere(filiere_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_promotions_by_filiere(db, filiere_id)

@router.post("/classes", response_model=ClassResponse, dependencies=[admin_dep])
async def api_create_class(data: ClassCreate, db: AsyncSession = Depends(get_db)):
    return await create_class(db, data)

@router.get("/classes/{promotion_id}", response_model=List[ClassResponse], dependencies=[admin_dep])
async def api_get_classes_by_promotion(promotion_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_classes_by_promotion(db, promotion_id)
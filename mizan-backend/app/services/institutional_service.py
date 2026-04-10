# CRUD operations for School, Filière, and Class institutional entities
# app/services/institutional_service.py
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.institution import Class, Filiere, Promotion, School
from app.schemas.institution import (
    ClassCreate,
    FiliereCreate,
    PromotionCreate,
    SchoolCreate,
)


async def create_school(db: AsyncSession, data: SchoolCreate) -> School:
    result = await db.execute(select(School).where(School.name == data.name))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="School with this name already exists"
        )
        
    school = School(name=data.name)
    db.add(school)
    await db.commit()
    await db.refresh(school)
    return school


async def get_all_schools(db: AsyncSession) -> list[School]:
    result = await db.execute(select(School))
    return list(result.scalars().all())


async def create_filiere(db: AsyncSession, data: FiliereCreate) -> Filiere:
    school_result = await db.execute(select(School).where(School.id == data.school_id))
    if not school_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="School not found"
        )

    filiere_result = await db.execute(
        select(Filiere).where(Filiere.name == data.name, Filiere.school_id == data.school_id)
    )
    if filiere_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Filiere with this name already exists in this school"
        )

    filiere = Filiere(name=data.name, school_id=data.school_id)
    db.add(filiere)
    await db.commit()
    await db.refresh(filiere)
    return filiere


async def get_filieres_by_school(db: AsyncSession, school_id: UUID) -> list[Filiere]:
    school_result = await db.execute(select(School).where(School.id == school_id))
    if not school_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="School not found"
        )

    result = await db.execute(select(Filiere).where(Filiere.school_id == school_id))
    return list(result.scalars().all())


async def create_promotion(db: AsyncSession, data: PromotionCreate) -> Promotion:
    filiere_result = await db.execute(select(Filiere).where(Filiere.id == data.filiere_id))
    if not filiere_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Filiere not found"
        )

    promo_result = await db.execute(
        select(Promotion).where(Promotion.name == data.name, Promotion.filiere_id == data.filiere_id)
    )
    if promo_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Promotion with this name already exists in this filiere"
        )

    promotion = Promotion(name=data.name, filiere_id=data.filiere_id)
    db.add(promotion)
    await db.commit()
    await db.refresh(promotion)
    return promotion


async def get_promotions_by_filiere(db: AsyncSession, filiere_id: UUID) -> list[Promotion]:
    filiere_result = await db.execute(select(Filiere).where(Filiere.id == filiere_id))
    if not filiere_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Filiere not found"
        )

    result = await db.execute(select(Promotion).where(Promotion.filiere_id == filiere_id))
    return list(result.scalars().all())


async def create_class(db: AsyncSession, data: ClassCreate) -> Class:
    promo_result = await db.execute(select(Promotion).where(Promotion.id == data.promotion_id))
    if not promo_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Promotion not found"
        )

    class_result = await db.execute(
        select(Class).where(Class.name == data.name, Class.promotion_id == data.promotion_id)
    )
    if class_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Class with this name already exists in this promotion"
        )

    new_class = Class(
        name=data.name, 
        promotion_id=data.promotion_id, 
        academic_year=data.academic_year
    )
    db.add(new_class)
    await db.commit()
    await db.refresh(new_class)
    return new_class


async def get_classes_by_promotion(db: AsyncSession, promotion_id: UUID) -> list[Class]:
    promo_result = await db.execute(select(Promotion).where(Promotion.id == promotion_id))
    if not promo_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Promotion not found"
        )

    result = await db.execute(select(Class).where(Class.promotion_id == promotion_id))
    return list(result.scalars().all())
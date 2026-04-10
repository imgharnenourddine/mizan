# Pydantic schemas for institutional entities — SchoolCreate, FiliereCreate, ClassCreate, responses
# app/schemas/institution.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SchoolCreate(BaseModel):
    name: str


class SchoolResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FiliereCreate(BaseModel):
    name: str
    school_id: UUID


class FiliereResponse(BaseModel):
    id: UUID
    name: str
    school_id: UUID

    model_config = ConfigDict(from_attributes=True)


class PromotionCreate(BaseModel):
    name: str
    filiere_id: UUID


class PromotionResponse(BaseModel):
    id: UUID
    name: str
    filiere_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ClassCreate(BaseModel):
    name: str
    promotion_id: UUID
    academic_year: str


class ClassResponse(BaseModel):
    id: UUID
    name: str
    promotion_id: UUID
    academic_year: str

    model_config = ConfigDict(from_attributes=True)
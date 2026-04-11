# app/schemas/resource.py
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.resource import ResourceType


class ResourceResponse(BaseModel):
    id: UUID
    title: str
    type: ResourceType
    url: str
    tags: List[str]
    mood_trigger: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
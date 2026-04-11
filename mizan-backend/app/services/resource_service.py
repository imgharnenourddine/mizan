# app/services/resource_service.py
from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource import ResourceType, WellbeingResource


async def get_resources_for_mood(db: AsyncSession, mood_score: int) -> List[WellbeingResource]:
    if mood_score in [1, 2]:
        triggers = ["anxiete", "stress"]
    elif mood_score == 3:
        triggers = ["motivation"]
    else:
        triggers = ["performance"]
        
    result = await db.execute(
        select(WellbeingResource).where(WellbeingResource.mood_trigger.in_(triggers))
    )
    return list(result.scalars().all())


async def get_all_resources(db: AsyncSession) -> List[WellbeingResource]:
    result = await db.execute(select(WellbeingResource))
    return list(result.scalars().all())


async def seed_default_resources(db: AsyncSession) -> None:
    result = await db.execute(select(func.count()).select_from(WellbeingResource))
    count = result.scalar() or 0
    
    if count == 0:
        defaults = [
            {
                "title": "Technique de respiration 4-7-8",
                "type": ResourceType.VIDEO,
                "url": "https://youtube.com/...",
                "tags": ["anxiete", "stress"],
                "mood_trigger": "anxiete"
            },
            {
                "title": "Méthode Pomodoro expliquée",
                "type": ResourceType.VIDEO,
                "url": "https://youtube.com/...",
                "tags": ["productivite", "revision"],
                "mood_trigger": "motivation"
            },
            {
                "title": "Comment améliorer son sommeil",
                "type": ResourceType.ARTICLE,
                "url": "https://...",
                "tags": ["sommeil", "repos"],
                "mood_trigger": "stress"
            },
            {
                "title": "Exercice de cohérence cardiaque",
                "type": ResourceType.EXERCISE,
                "url": "https://...",
                "tags": ["stress", "anxiete"],
                "mood_trigger": "anxiete"
            },
            {
                "title": "Techniques de mémorisation efficaces",
                "type": ResourceType.ARTICLE,
                "url": "https://...",
                "tags": ["revision", "performance"],
                "mood_trigger": "performance"
            }
        ]
        
        for r_data in defaults:
            resource = WellbeingResource(
                title=r_data["title"],
                type=r_data["type"],
                url=r_data["url"],
                tags=r_data["tags"],
                mood_trigger=r_data["mood_trigger"]
            )
            db.add(resource)
            
        await db.commit()
# Mizan AI agent endpoints — generate daily plan, get proactive insights via Mistral AI
# app/api/v1/routes/agent.py
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from mistralai import Mistral

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.agent_service import generate_daily_plan
from app.services.context_builder import build_agent_context
from app.services.student_service import get_student_by_user_id

settings = get_settings()

router = APIRouter(prefix="/agent", tags=["Agent"])


class PlanRequest(BaseModel):
    sleep_hours: float
    mood_score: int


class ChatRequest(BaseModel):
    message: str


@router.get("/context")
async def api_get_context(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    return await build_agent_context(db, student.id)


@router.post("/plan")
async def api_generate_plan(
    data: PlanRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    context = await build_agent_context(db, student.id)
    plan = await generate_daily_plan(context, data.sleep_hours, data.mood_score)
    return {"plan": plan}


@router.post("/chat")
async def api_chat_agent(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    student = await get_student_by_user_id(db, current_user.id)
    context = await build_agent_context(db, student.id)
    
    client = Mistral(api_key=settings.MISTRAL_API_KEY)
    
    context_str = json.dumps(context, default=str, ensure_ascii=False)
    
    prompt = f"""You are Mizan, an empathetic AI student wellbeing assistant.
You are talking to {context.get('student', {}).get('name', 'a student')}.

Here is the student's current context:
{context_str}

Student's message:
"{data.message}"

Respond directly to the student in a helpful, supportive, and concise manner based on their context.
"""

    response = await client.chat.complete_async(
        model=settings.MISTRAL_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return {"response": response.choices[0].message.content}
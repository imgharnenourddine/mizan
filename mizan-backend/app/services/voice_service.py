# app/services/voice_service.py
import base64
import json
import uuid
from datetime import date, datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from mistralai import Mistral
from elevenlabs.client import AsyncElevenLabs
from groq import AsyncGroq

from app.core.config import get_settings
from app.models.checkin import EveningCheckin, MorningCheckin
from app.models.student import Exam, Project, Schedule
from app.schemas.voice import (
    VoiceAnalysisResponse,
    VoiceQuestion,
    VoiceSessionResponse,
    VoiceSessionSubmit,
)
from app.services.checkin_service import has_morning_checkin_today

settings = get_settings()


async def get_questions_for_student(db: AsyncSession, student_id: UUID, period: str) -> List[str]:
    today = date.today()
    questions = []

    if period == "MORNING":
        questions.extend([
            "Comment tu as dormi cette nuit ?",
            "Comment tu te sens émotionnellement ce matin ?"
        ])

        day_name = today.strftime("%A")
        sched_res = await db.execute(
            select(Schedule).where(and_(Schedule.student_id == student_id, Schedule.day_of_week == day_name))
        )
        if first_course := sched_res.scalars().first():
            questions.append(f"Tu as {first_course.subject} ce matin avec {first_course.professor}, tu es prêt ?")

        two_days_later = today + timedelta(days=2)
        exam_res = await db.execute(
            select(Exam).where(and_(Exam.student_id == student_id, Exam.exam_date >= today, Exam.exam_date <= two_days_later))
        )
        for exam in exam_res.scalars().all():
            days_left = (exam.exam_date - today).days
            questions.append(f"Ton examen de {exam.subject} est dans {days_left} jours, tu te sens prêt ?")

        project_res = await db.execute(
            select(Project).where(and_(Project.student_id == student_id, Project.due_date >= today, Project.due_date <= two_days_later))
        )
        for project in project_res.scalars().all():
            days_left = (project.due_date - today).days
            questions.append(f"Ton projet {project.name} est à rendre dans {days_left} jours, où tu en es ?")

    elif period == "EVENING":
        questions.extend([
            "Comment s'est passée ta journée ?",
            "Tu as pu accomplir ce que tu avais prévu ?",
            "Comment tu te sens en fin de journée ?"
        ])

        has_morning = await has_morning_checkin_today(db, student_id)
        if has_morning:
            questions.append("Par rapport à ce matin, tu te sens mieux ou moins bien ?")

    return questions[:4]


async def text_to_speech(text: str) -> bytes:
    settings = get_settings()
    
    from elevenlabs import ElevenLabs
    
    client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
    
    audio = client.text_to_speech.convert(
        voice_id=settings.ELEVENLABS_VOICE_ID,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    audio_bytes = b""
    for chunk in audio:
        audio_bytes += chunk
    
    return audio_bytes


async def speech_to_text(audio_bytes: bytes) -> str:
    if not settings.GROQ_API_KEY:
        return ""
        
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    response = await client.audio.transcriptions.create(
        file=("audio.wav", audio_bytes),
        model="whisper-large-v3",
        language="fr"
    )
    return response.text


async def start_voice_session(db: AsyncSession, student_id: UUID, period: str) -> VoiceSessionResponse:
    if period not in ["MORNING", "EVENING"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Period must be MORNING or EVENING")
        
    raw_questions = await get_questions_for_student(db, student_id, period)
    
    questions = []
    for idx, text in enumerate(raw_questions):
        questions.append(VoiceQuestion(index=idx, text=text))
        
    first_audio_bytes = await text_to_speech(questions[0].text) if questions else b""
    first_audio_base64 = base64.b64encode(first_audio_bytes).decode("utf-8") if first_audio_bytes else ""
    
    return VoiceSessionResponse(
        session_id=str(uuid.uuid4()),
        questions=questions,
        first_audio_base64=first_audio_base64
    )


async def transcribe_audio(audio_file: UploadFile) -> str:
    audio_bytes = await audio_file.read()
    return await speech_to_text(audio_bytes)


async def analyze_voice_responses(db: AsyncSession, student_id: UUID, data: VoiceSessionSubmit) -> VoiceAnalysisResponse:
    client = Mistral(api_key=settings.MISTRAL_API_KEY)
    
    transcriptions_text = "\n".join([f"Q{t.question_index}: {t.transcription}" for t in data.transcriptions])
    
    prompt = f"""Analyze the following transcribed voice responses from a student for their {data.period} check-in.
    
Transcriptions:
{transcriptions_text}

Extract the following information and return exactly a JSON object with these keys:
- "mood_score": an integer from 1 to 5 representing their overall mood.
- "sleep_hours": a float representing hours of sleep (or null if not mentioned).
- "plan_completed": a boolean indicating if they completed their daily plan (only relevant for EVENING, default to false if unclear).
- "analysis": a short string summarizing their state and thoughts.
- "recommendations": a list of strings containing 2-3 specific, actionable recommendations for them.

JSON format only. No markdown formatting.
"""

    response = await client.chat.complete_async(
        model=settings.MISTRAL_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        content = response.choices[0].message.content
        parsed_data = json.loads(content)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to parse AI analysis")
        
    mood_score = parsed_data.get("mood_score", 3)
    sleep_hours = parsed_data.get("sleep_hours")
    plan_completed = parsed_data.get("plan_completed", False)
    analysis_text = parsed_data.get("analysis", "No analysis available")
    recommendations = parsed_data.get("recommendations", [])

    if data.period == "MORNING":
        checkin = MorningCheckin(
            student_id=student_id,
            date=date.today(),
            sleep_hours=sleep_hours if sleep_hours is not None else 0.0,
            mood_score=mood_score,
            generated_plan=analysis_text
        )
    else:
        checkin = EveningCheckin(
            student_id=student_id,
            date=date.today(),
            plan_completed=plan_completed,
            mood_score=mood_score,
            notes=analysis_text
        )
        
    db.add(checkin)
    await db.commit()
    await db.refresh(checkin)
    
    return VoiceAnalysisResponse(
        analysis=analysis_text,
        mood_score=mood_score,
        sleep_hours=sleep_hours,
        recommendations=recommendations,
        saved_checkin_id=checkin.id
    )
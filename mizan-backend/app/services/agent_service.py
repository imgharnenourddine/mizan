# Mistral AI API call orchestration — send context, receive completion, parse daily plan
# app/services/agent_service.py
from mistralai import Mistral

from app.core.config import get_settings

settings = get_settings()


async def generate_daily_plan(context: dict, sleep_hours: float, mood_score: int) -> str:
    client = Mistral(api_key=settings.MISTRAL_API_KEY)
    
    schedule_text = "\n".join([f"- {s.subject} ({s.start_time} - {s.end_time}) in {s.room} with {s.professor}" for s in context.get("today_schedule", [])])
    exams_text = "\n".join([f"- {e.subject} on {e.exam_date} ({e.start_time} - {e.end_time})" for e in context.get("upcoming_exams", [])])
    projects_text = "\n".join([f"- {p.name} ({p.subject}) due on {p.due_date}" for p in context.get("upcoming_projects", [])])
    
    last_evening_mood = context.get("last_evening_mood")
    mood_context = f"Last evening's mood was {last_evening_mood}/5." if last_evening_mood else "No previous evening mood recorded."

    prompt = f"""You are Mizan, an empathetic AI student wellbeing assistant.
Create a supportive and structured daily plan for a student based on the following context:

Today's Schedule:
{schedule_text if schedule_text else "No classes scheduled today."}

Upcoming Exams (next 3 days):
{exams_text if exams_text else "None."}

Upcoming Project Deadlines (next 5 days):
{projects_text if projects_text else "None."}

Student Wellbeing:
- Sleep last night: {sleep_hours} hours
- Morning mood: {mood_score}/5
- {mood_context}

Provide a short, motivating, and actionable daily plan. If they slept poorly or have low mood, suggest breaks and self-care. If they have exams/projects, suggest specific revision modes. Address the student directly. Keep it under 200 words.
"""

    response = await client.chat.complete_async(
        model=settings.MISTRAL_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content
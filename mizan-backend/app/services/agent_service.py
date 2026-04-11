# app/services/agent_service.py
from mistralai import Mistral

from app.core.config import get_settings

settings = get_settings()


async def generate_daily_plan(context: dict, sleep_hours: float, mood_score: int) -> str:
    client = Mistral(api_key=settings.MISTRAL_API_KEY)
    
    schedule = context.get("today_schedule", [])
    schedule_text = "\n".join([f"- {s['subject']} ({s['start_time']} - {s['end_time']}) in {s['room']} with {s['professor']}" for s in schedule])
    
    exams = context.get("upcoming_exams", [])
    exams_text = "\n".join([f"- {e['subject']} on {e['exam_date']} (in {e['days_until']} days)" for e in exams])
    
    projects = context.get("upcoming_projects", [])
    projects_text = "\n".join([f"- {p['name']} ({p['subject']}) due on {p['due_date']} (in {p['days_until']} days)" for p in projects])
    
    goals = context.get("active_goals", [])
    goals_text = "\n".join([f"- {g['title']} (Target: {g['target_value']} {g['unit']})" for g in goals])
    
    stress = context.get("stress_indicators", {})
    stress_text = f"""
    - Exam tomorrow: {stress.get('has_exam_tomorrow', False)}
    - Exam this week: {stress.get('has_exam_this_week', False)}
    - Overdue projects: {stress.get('overdue_projects', 0)}
    - Consecutive low mood days: {stress.get('consecutive_low_mood_days', 0)}
    """
    
    last_checkin = context.get("last_checkin")
    last_evening_mood = last_checkin.get("mood_score") if last_checkin else None
    mood_context = f"Last check-in mood was {last_evening_mood}/5." if last_evening_mood else "No previous check-in mood recorded."

    prompt = f"""You are Mizan, an empathetic AI student wellbeing assistant.
Create a supportive and structured daily plan for a student based on the following context:

Today's Schedule:
{schedule_text if schedule_text else "No classes scheduled today."}

Upcoming Exams:
{exams_text if exams_text else "None."}

Upcoming Project Deadlines:
{projects_text if projects_text else "None."}

Active Goals:
{goals_text if goals_text else "None."}

Stress Indicators:
{stress_text}

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
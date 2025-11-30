from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import QuizScore, User, ChatHistory, UserTopic
from backend.auth import get_current_user
from pydantic import BaseModel
import google.generativeai as genai
import os
import random

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
)

class ScoreCreate(BaseModel):
    topic: str
    score: int
    total_questions: int

class QuizRequest(BaseModel):
    topic: Optional[str] = None
    from_history: bool = False

@router.get("/has-topics")
def has_topics(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(UserTopic).where(UserTopic.user_id == current_user.id).limit(1)
    result = session.exec(statement).first()
    return {"has_topics": result is not None}

@router.post("/generate")
def generate_quiz(request: QuizRequest, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    topic = request.topic
    
    if request.from_history:
        # Fetch random topics from UserTopic (up to 5 unique ones)
        statement = select(UserTopic).where(UserTopic.user_id == current_user.id)
        topics_records = session.exec(statement).all()
        if topics_records:
            # Get unique topics to avoid duplicates
            unique_topics = list(set([t.topic for t in topics_records]))
            # Sample up to 5 topics
            selected_topics = random.sample(unique_topics, k=min(len(unique_topics), 5))
            topic = ", ".join(selected_topics)
            prompt_topic = f"a mixed quiz covering these topics: {topic}"
        else:
            raise HTTPException(status_code=400, detail="No study history found. Please use Chat or Summarizer first.")
    else:
        if not topic:
            topic = "General Knowledge"
        prompt_topic = f"'{topic}'"

    # Use Gemini to generate quiz
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API not configured")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    
    prompt = f"""Generate a quiz with 5 multiple choice questions about {prompt_topic}.
    Format the output strictly as a JSON list of objects with keys: 'question', 'options' (list of 4 strings), 'answer' (correct option string).
    IMPORTANT: The 'options' list must NOT indicate which answer is correct (e.g., do NOT add "(Correct)" or "*" to the option text). The options should be plain text.
    The 'answer' field must match one of the options exactly.
    Do not include markdown formatting like ```json. Just the raw JSON string.
    """
    
    try:
        response = model.generate_content(prompt)
        import json
        quiz_data = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        return {"topic": topic, "questions": quiz_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@router.post("/score", response_model=QuizScore)
def save_score(score_data: ScoreCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    score = QuizScore(
        topic=score_data.topic,
        score=score_data.score,
        total_questions=score_data.total_questions,
        user_id=current_user.id
    )
    session.add(score)
    session.commit()
    session.refresh(score)
    return score

@router.get("/history", response_model=List[QuizScore])
def get_history(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(QuizScore).where(QuizScore.user_id == current_user.id).order_by(QuizScore.timestamp.desc())
    results = session.exec(statement)
    return results.all()

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import ChatHistory, User, UserTopic
from backend.auth import get_current_user

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.5-flash")
else:
    model = None

router = APIRouter(
    prefix="/ai",
    tags=["ai"],
)

class ChatRequest(BaseModel):
    message: str

class SummaryRequest(BaseModel):
    text: str

def extract_and_save_topic(text: str, user_id: int, session: Session):
    """Extracts a main topic from text and saves it to UserTopic."""
    if not model:
        return
    try:
        # Ask Gemini to extract a single short topic
        prompt = f"Extract one main educational topic or subject (1-3 words max) from this text. Return ONLY the topic name, nothing else. Text: {text[:500]}"
        response = model.generate_content(prompt)
        topic = response.text.strip()
        
        if topic and len(topic) < 50: # Basic validation
            # Check if topic already exists recently to avoid spamming (optional, but good for now just add it)
            # For simplicity, we just add it. The quiz logic will pick randomly.
            user_topic = UserTopic(topic=topic, user_id=user_id)
            session.add(user_topic)
            session.commit()
    except Exception as e:
        print(f"Error extracting topic: {e}")

@router.post("/chat")
def chat(request: ChatRequest, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API not configured")
    try:
        response = model.generate_content(request.message)
        ai_response = response.text
        
        # Save history
        history = ChatHistory(query=request.message, response=ai_response, user_id=current_user.id)
        session.add(history)
        session.commit()
        
        # Extract topic in background
        background_tasks.add_task(extract_and_save_topic, request.message + " " + ai_response, current_user.id, session)
        
        return {"response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
def summarize(request: SummaryRequest, background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API not configured")
    try:
        prompt = f"Summarize the following text:\n\n{request.text}"
        response = model.generate_content(prompt)
        summary = response.text
        
        # Extract topic in background
        background_tasks.add_task(extract_and_save_topic, request.text, current_user.id, session)
        
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

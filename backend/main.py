from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Added this import
from backend.database import create_db_and_tables
from backend.routers import auth, ai, quiz, notes

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(quiz.router)
app.include_router(notes.router)
app.include_router(quiz.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI StudyBuddy API"}

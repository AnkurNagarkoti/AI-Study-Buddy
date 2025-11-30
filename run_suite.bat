@echo off
echo Starting Backend...
start "AI StudyBuddy Backend" cmd /k "python -m uvicorn backend.main:app --reload --port 8000"

echo Starting Frontend...
start "AI StudyBuddy Frontend" cmd /k "python -m streamlit run frontend/main.py --server.port 8501"

echo App is starting! Please wait a moment for both windows to initialize.

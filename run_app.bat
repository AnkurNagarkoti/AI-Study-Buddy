@echo off
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

if not exist .env (
    echo Creating .env file...
    echo GEMINI_API_KEY=YOUR_API_KEY_HERE > .env
)

echo Starting Streamlit app...
streamlit run frontend/main.py

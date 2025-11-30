# AI Study Buddy - Startup Guide

This guide explains how to start and stop the AI Study Buddy application (Frontend, Backend, and Database).

## Prerequisites

- Python 3.10+ installed.
- Internet connection (for AI features).

## 1. First Time Setup

Before running the app for the first time, install the required dependencies:

```bash
pip install -r requirements.txt
```

*Note: If you encounter issues with `pyarrow` on Python 3.14, use the nightly build:*
```bash
pip install --extra-index-url https://pypi.fury.io/arrow-nightlies/ --pre pyarrow
pip install streamlit
```

## 2. Starting the Application

### Option A: The Easy Way (Windows Batch Script)

We have created a script that launches both the backend and frontend for you.

1.  Double-click **`run_suite.bat`** in the project folder.
2.  Two command prompt windows will open (one for Backend, one for Frontend).
3.  The browser should automatically open to the application.

### Option B: Manual Start (Terminal)

If you prefer to run commands manually, you need two separate terminal windows.

**Terminal 1: Backend (API & Database)**
This starts the FastAPI server and initializes the SQLite database (`studybuddy.db`).
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
*Wait until you see "Application startup complete".*

**Terminal 2: Frontend (UI)**
This starts the Streamlit user interface.
```bash
python -m streamlit run frontend/main.py
```

## 3. Database

The application uses **SQLite**, which is a file-based database.
- The database file `studybuddy.db` is automatically created in the project root directory when you start the backend.
- No manual setup is required.

## 4. How to Close/Stop the Project

To stop the application:

1.  Go to the terminal windows running the Backend and Frontend.
2.  Press **`Ctrl + C`** in each window to stop the server.
3.  Close the terminal windows.

---
**Troubleshooting:**
- If the frontend says "Connection Refused", make sure the Backend (Terminal 1) is running.
- If you see "ModuleNotFoundError", make sure you ran the installation steps in Section 1.

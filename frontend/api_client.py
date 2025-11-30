import requests
import streamlit as st
import PyPDF2
import io

API_URL = "http://localhost:8000"

def extract_text_from_pdf(file_bytes):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def login(username, password):
    response = requests.post(f"{API_URL}/auth/token", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()
    return None

def register(username, password):
    response = requests.post(f"{API_URL}/auth/register", json={"username": username, "hashed_password": password})
    return response.status_code == 200

def get_headers():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

@st.cache_data(ttl=10, show_spinner=False)
def get_notes():
    response = requests.get(f"{API_URL}/notes/", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []

def create_note(title, content, folder="General"):
    response = requests.post(f"{API_URL}/notes/", json={"title": title, "content": content, "folder": folder}, headers=get_headers())
    if response.status_code == 200:
        get_notes.clear() # Clear cache on update
        get_folders.clear()
        return True
    return False

def delete_note(note_id):
    response = requests.delete(f"{API_URL}/notes/{note_id}", headers=get_headers())
    if response.status_code == 200:
        get_notes.clear() # Clear cache on update
        return True
    return False

def chat_with_ai(message):
    response = requests.post(f"{API_URL}/ai/chat", json={"message": message}, headers=get_headers())
    if response.status_code == 200:
        return response.json().get("response")
    return "Error contacting AI."

def summarize_text(text):
    response = requests.post(f"{API_URL}/ai/summarize", json={"text": text}, headers=get_headers())
    if response.status_code == 200:
        return response.json().get("summary")
    return "Error generating summary."

def save_quiz_score(topic, score, total):
    response = requests.post(f"{API_URL}/quiz/score", json={"topic": topic, "score": score, "total_questions": total}, headers=get_headers())
    return response.status_code == 200

@st.cache_data(ttl=10, show_spinner=False)
def get_quiz_history():
    response = requests.get(f"{API_URL}/quiz/history", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return []

def check_has_topics():
    response = requests.get(f"{API_URL}/quiz/has-topics", headers=get_headers())
    if response.status_code == 200:
        return response.json().get("has_topics", False)
    return False

def generate_quiz(topic=None, from_history=False):
    response = requests.post(f"{API_URL}/quiz/generate", json={"topic": topic, "from_history": from_history}, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None

@st.cache_data(ttl=10, show_spinner=False)
def get_folders():
    response = requests.get(f"{API_URL}/notes/folders", headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return ["General"]

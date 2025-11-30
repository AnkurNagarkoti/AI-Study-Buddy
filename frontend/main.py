import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import extra_streamlit_components as stx
from frontend.views.auth import auth_page
from frontend.views.dashboard import dashboard_page
from frontend.views.notes import notes_page
from frontend.views.study import study_page
import time

# Page Config
st.set_page_config(page_title="AI StudyBuddy", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")

# Cookie Manager
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

# Session State Initialization
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Auth"

# Check for cookies on load
cookies = cookie_manager.get_all()
if not st.session_state.token and "token" in cookies:
    st.session_state.token = cookies["token"]
    if "username" in cookies:
        st.session_state.username = cookies["username"]
    st.rerun()

# Navigation Logic
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def logout():
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.current_page = "Auth"
    cookie_manager.delete("token")
    cookie_manager.delete("username")
    time.sleep(1) # Wait for cookie deletion
    st.rerun()

# Sidebar (Only show if logged in)
if st.session_state.token:
    with st.sidebar:
        # Display Username in Uppercase
        display_name = st.session_state.username.upper() if st.session_state.username else "USER"
        st.title(f"👤 {display_name}")
        st.markdown("---")
        
        if st.button("📊 Dashboard", use_container_width=True):
            navigate_to("Dashboard")
        if st.button("🧠 Study Room", use_container_width=True):
            navigate_to("Study Room")
        if st.button("📝 Notes", use_container_width=True):
            navigate_to("Notes")
            
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
else:
    # Hide sidebar on login page via CSS
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

# Main Content Routing
if st.session_state.token:
    if st.session_state.current_page == "Dashboard":
        dashboard_page()
    elif st.session_state.current_page == "Study Room":
        study_page()
    elif st.session_state.current_page == "Notes":
        notes_page()
    else:
        dashboard_page() # Default to dashboard
else:
    auth_page(cookie_manager)

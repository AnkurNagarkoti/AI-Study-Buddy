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
if 'logout_pending' not in st.session_state:
    st.session_state.logout_pending = False

# Handle logout completion after page reload
if st.session_state.logout_pending:
    # Clear session state after cookies have been cleared by JavaScript
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.current_page = "Auth"
    st.session_state.logout_pending = False
    st.rerun()

# Check for cookies on load (only if not logging out)
if not st.session_state.logout_pending:
    cookies = cookie_manager.get_all(key="get_all")
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
    """
    Two-phase logout function:
    Phase 1: Clear cookies with JavaScript and reload page
    Phase 2: Clear session state after reload
    """
    # Set logout pending flag
    st.session_state.logout_pending = True
    
    # Delete cookies using cookie_manager (server-side)
    try:
        current_cookies = cookie_manager.get_all(key="get_all_logout")
        
        if "token" in current_cookies:
            cookie_manager.delete("token", key="delete_token")
        
        if "username" in current_cookies:
            cookie_manager.delete("username", key="delete_username")
    except Exception as e:
        # Log error but continue with logout
        pass
    
    # Use JavaScript to clear all client-side storage, cookies, and reload
    st.components.v1.html(
        """
        <script>
            (function() {
                try {
                    // Clear localStorage and sessionStorage
                    window.localStorage.clear();
                    window.sessionStorage.clear();
                    
                    // Delete specific cookies by name
                    function deleteCookie(name) {
                        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + window.location.hostname + ';';
                    }
                    
                    deleteCookie('token');
                    deleteCookie('username');
                    
                    // Also clear all cookies as a fallback
                    document.cookie.split(';').forEach(function(cookie) {
                        var name = cookie.split('=')[0].trim();
                        deleteCookie(name);
                    });
                    
                    // Reload page after clearing cookies (this ensures cookies are cleared before next run)
                    setTimeout(function() {
                        window.location.href = window.location.pathname;
                    }, 100);
                } catch (e) {
                    console.error('Logout cleanup error:', e);
                    // Still reload even if there's an error
                    window.location.href = window.location.pathname;
                }
            })();
        </script>
        """,
        height=0,
    )

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

import streamlit as st
from frontend.api_client import login, register

def auth_page(cookie_manager=None):
    st.title("🔐 Login / Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username and password:
                response = login(username, password)
                if response:
                    token = response["access_token"]
                    st.session_state.token = token
                    st.session_state.username = username
                    
                    if cookie_manager:
                        cookie_manager.set("token", token, key="set_token")
                        cookie_manager.set("username", username, key="set_user")
                    
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.warning("Please fill in all fields")

    with tab2:
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            if new_user and new_pass:
                if register(new_user, new_pass):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed (Username might be taken)")
            else:
                st.warning("Please fill in all fields")

import streamlit as st
import sys
import os

st.title("Environment Diagnosis")

st.write(f"**Python Executable:** `{sys.executable}`")
st.write(f"**Current Working Directory:** `{os.getcwd()}`")

st.subheader("Sys Path:")
for p in sys.path:
    st.write(f"- `{p}`")

st.subheader("Import Check:")
try:
    import matplotlib
    st.success(f"✅ matplotlib found at `{matplotlib.__file__}`")
except ImportError as e:
    st.error(f"❌ matplotlib NOT found: {e}")

try:
    import dotenv
    st.success(f"✅ dotenv found at `{dotenv.__file__}`")
except ImportError as e:
    st.error(f"❌ dotenv NOT found: {e}")

# streamlit_app/app.py

import streamlit as st
import requests
import tempfile
import os

st.set_page_config(page_title="🧠 Finance Assistant", layout="centered")

FASTAPI_URL = "http://localhost:8000"

st.title("📊 Morning Market Brief (AI Assistant)")
st.markdown("Ask about **Asia tech stock exposure** and **earnings surprises**.")

mode = st.radio("Input Mode", ["Text", "Voice"])

if mode == "Text":
    query = st.text_input("Enter your question", value="What’s our risk exposure in Asia tech stocks today?")
    if st.button("Get Market Brief"):
        try:
            res = requests.post(f"{FASTAPI_URL}/brief/text", json={"query": query})
            if res.status_code == 200:
                st.success(res.json()["response"])
            else:
                st.error(f"Failed to fetch brief: {res.text}")
        except Exception as e:
            st.error(f"Error: {e}")

else:
    uploaded_file = st.file_uploader("Upload voice (.wav only)", type=["wav"])
    if st.button("Analyze Voice"):
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            try:
                with open(tmp_path, "rb") as f:
                    files = {"file": f}
                    res = requests.post(f"{FASTAPI_URL}/brief/voice", files=files)
                if res.status_code == 200:
                    data = res.json()
                    st.write("🗣️ You said:", data["transcription"])
                    st.success(data["response"])
                else:
                    st.error(f"Failed to process voice input: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                os.remove(tmp_path)
        else:
            st.warning("Please upload a .wav file first.")



import streamlit as st
import cohere
import PyPDF2
import docx2txt
from dotenv import load_dotenv
import os

# === Load Environment Variables ===
load_dotenv()
api_key = os.getenv("API_KEY") or st.secrets.get("API_KEY")

# === Initialize Cohere Client ===
if not api_key:
    st.error("🚨 Cohere API key not found. Please set it in your .env file.")
    st.stop()
co = cohere.Client(api_key)

# === Page Config ===
st.set_page_config(page_title="Resume Matcher", page_icon="🧠", layout="centered")

# === Text Extraction ===
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return ''.join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return "❌ Unsupported file type."

# === Cohere Analysis ===
def analyze_resume_vs_jd(resume_text, jd_text):
    prompt = f"""
You are a job matching assistant.

Here is the resume:
{resume_text}

Here is the job description:
{jd_text}

Compare them and give:
- Match score (0-100)
- List of missing or weak keywords in resume
- Suggestions to improve the resume for this JD
Respond in bullet points only.
"""
    response = co.chat(model="command-r-plus", message=prompt)
    return response.text

# === Streamlit UI ===
st.title("🎯 Resume vs JD Analyzer")
st.markdown("Upload your **Resume** and paste your **Job Description** to see how well they match!")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_upload")
with col2:
    jd_text = st.text_area("📃 Job Description (Paste text here)", "")


if resume_file and jd_text.strip():
    st.success("✅ Inputs ready. Click below to analyze.")
    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing with AI..."):
            resume_text = extract_text(resume_file)
            result = analyze_resume_vs_jd(resume_text, jd_text)
        st.subheader("📊 Result")
        st.markdown(
            f"<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;color:#333;'>{result.replace('-', '🔹')}</div>",
            unsafe_allow_html=True
        )

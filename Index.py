

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
import re
import streamlit as st

# 💡 Use the actual result from your AI
result = """🔹 Match Score: 35/100 🔹 Missing/Weak Keywords: 🔹 Microsoft Office 🔹 Excel 🔹 Data Analysis 🔹 WIP management 🔹 Training program development 🔹 Process improvements 🔹 High🔹value/high🔹risk item handling 🔹 Network expansion 🔹 Suggestions: 🔹 Emphasize basic knowledge in SQL, programming, and data analysis to align with the job requirements. 🔹 Highlight any experience with Microsoft Office products and applications, especially Excel. 🔹 Consider including projects or experiences related to process improvement, training program development, or network expansion to better match the preferred qualifications. 🔹 Focus on transferable skills such as problem🔹solving, adaptability, and collaboration, which are valuable in various roles. 🔹 Tailor the resume to highlight relevant skills and experiences that match the job responsibilities and qualifications."""

# ✅ 1. Clean splits using regex
match_score = re.search(r"Match Score: (.+?)🔹", result)
match_score_text = match_score.group(1).strip() if match_score else "❌ Not found"

keywords_section = re.search(r"Missing/Weak Keywords:(.+?)Suggestions:", result)
keywords_text = keywords_section.group(1).strip() if keywords_section else "❌ Not found"

suggestions_section = re.search(r"Suggestions:(.+)", result)
suggestions_text = suggestions_section.group(1).strip() if suggestions_section else "❌ Not found"

# ✅ 2. Format bullets
def format_bullets(text):
    lines = re.split(r"🔹", text)
    return "".join(f"<li>{line.strip()}</li>" for line in lines if line.strip())

# ✅ 3. Display in separate sections
st.markdown(f"""
<div style='background-color:#e3f2fd;padding:15px;border-radius:10px;margin-bottom:15px;'>
  <h4 style='color:#0d47a1;'>🔹 Match Score</h4>
  <p style='margin:0;font-size:16px;color:#000000;'>{match_score_text}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='background-color:#fce4ec;padding:15px;border-radius:10px;margin-bottom:15px;'>
  <h4 style='color:#880e4f;'>🔹 Missing / Weak Keywords</h4>
  <ul style='color:#000000;'>{format_bullets(keywords_text)}</ul>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='background-color:#e8f5e9;padding:15px;border-radius:10px;'>
  <h4 style='color:#1b5e20;'>🔹 Suggestions to Improve Resume</h4>
  <ul style='color:#000000;'>{format_bullets(suggestions_text)}</ul>
</div>
""", unsafe_allow_html=True)

# st.markdown(
#     f"""
#     <div style='background-color:#fce4ec;padding:15px;border-radius:10px;margin-bottom:15px;'>
#         <h4 style='color:#880e4f;'>🔹 Missing / Weak Keywords</h4>
#         <p style='color:#000000;'>{keywords_section.replace('-', '🔹 ')}</p>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown(
#     f"""
#     <div style='background-color:#e8f5e9;padding:15px;border-radius:10px;'>
#         <h4 style='color:#1b5e20;'>🔹 Suggestions to Improve Resume</h4>
#         <p style='color:#000000;'>{suggestions_section.replace('-', '🔹 ')}</p>
#     </div>
#     """, unsafe_allow_html=True)


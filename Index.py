# 1. Import Libraries
import streamlit as st
import cohere
import PyPDF2
import docx2txt
from dotenv import load_dotenv
import os
import re

# 2. Load API Key (from .env or Streamlit Secrets)
load_dotenv()
api_key = os.getenv("API_KEY") or st.secrets.get("API_KEY")

if not api_key:
    st.error("🚨 Cohere API key not found. Please set it in a .env file or Streamlit Cloud secrets.")
    st.stop()

# 3. Initialize Cohere
co = cohere.Client(api_key)

# 4. Streamlit Page Config
st.set_page_config(page_title="Resume Matcher", page_icon="🧠", layout="centered")
st.title("🎯 Resume vs JD Analyzer")
st.markdown("Upload your **Resume** and paste your **Job Description** to see how well they match!")

# 5. Text Extraction Function
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return ''.join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return "❌ Unsupported file type."

# 6. Cohere Prompt Function
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

# 7. File Upload UI
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_upload")
with col2:
    jd_text = st.text_area("📃 Job Description (Paste text here)", "")

# 8. Analyze Button Logic
if resume_file and jd_text.strip():
    st.success("✅ Inputs ready. Click below to analyze.")
    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing with AI..."):
            resume_text = extract_text(resume_file)
            result = analyze_resume_vs_jd(resume_text, jd_text)
import re

# === Parse the Result ===
try:
    match_score_section = result.split("Missing/Weak Keywords:")[0].strip()
    keywords_section = result.split("Missing/Weak Keywords:")[1].split("Suggestions to Improve")[0].strip()
    suggestions_section = result.split("Suggestions to Improve")[1].strip()
except IndexError:
    st.error("⚠️ Error parsing AI output. Please try again.")
    st.stop()

# === Extract Match Score ===
match = re.search(r"(\d+)/100", match_score_section)
score = int(match.group(1)) if match else 0

# === Progress Bar ===
st.subheader("📊 Match Score")
st.progress(score / 100)

# === Helper to Build HTML List ===
def build_html_list(text):
    # Use either "🔹" or newlines as separators
    items = [line.strip("🔹- \n") for line in text.splitlines() if line.strip()]
    return ''.join(f"<li>{item}</li>" for item in items if item)

# === Final Styled Output ===
styled_output = f"""
<div style="background-color:#e3f2fd;padding:15px;border-radius:10px;margin-bottom:10px;">
    <h4 style="color:#000000;">🔹 Match Score</h4>
    <p style="font-size:18px; color:#000000;">{match_score_section}</p>
</div>

<div style="background-color:#fce4ec;padding:15px;border-radius:10px;margin-bottom:10px;">
    <h4 style="color:#000000;">🔹 Missing / Weak Keywords</h4>
    <ul style="background-color:#e8f5e9;color:#000000;padding:10px;border-radius:8px;margin:0;">
        {build_html_list(keywords_section)}
    </ul>
</div>

<div style="background-color:#e8f5e9;padding:15px;border-radius:10px;">
    <h4 style="color:#000000;">🔹 Suggestions to Improve Resume</h4>
    <ul style="background-color:#e8f5e9;color:#000000;padding:10px;border-radius:8px;margin:0;">
        {build_html_list(suggestions_section)}
    </ul>
</div>
"""

st.markdown(styled_output, unsafe_allow_html=True)

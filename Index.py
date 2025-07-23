import streamlit as st
import cohere
import PyPDF2
import docx2txt
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Resume Matcher", page_icon="🧠", layout="centered")
st.title("🎯 Resume vs JD Analyzer")
st.markdown("Upload your **Resume** and **Job Description** to see how well they match!")
load_dotenv()
api_key = os.getenv("API_KEY")
co = cohere.Client(api_key)

for key in ['result', 'resume_text', 'jd_text']:
    if key not in st.session_state:
        st.session_state[key] = ""

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return ''.join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return "Unsupported file type."
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

# === Inputs ===
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
with col2:
    jd_input = st.text_area("📃 Job Description", st.session_state.jd_text)

if resume_file and jd_input:
    st.success("✅ Inputs received. Click Analyze to proceed.")
    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing..."):
            resume_text = extract_text(resume_file)
            jd_text = jd_input

            st.session_state.resume_text = resume_text
            st.session_state.jd_text = jd_text
            st.session_state.result = analyze_resume_vs_jd(resume_text, jd_text)

if st.session_state.result:
    result = st.session_state.result

    # Split result using bullet sections
    import re
    match_score = re.search(r"Match Score: (.+?)🔹", result)
    match_score_text = match_score.group(1).strip() if match_score else "❌ Not found"

    keywords_section = re.search(r"Missing/Weak Keywords:(.+?)Suggestions:", result)
    keywords_text = keywords_section.group(1).strip() if keywords_section else "❌ Not found"

    suggestions_section = re.search(r"Suggestions:(.+)", result)
    suggestions_text = suggestions_section.group(1).strip() if suggestions_section else "❌ Not found"

    def format_bullets(text):
        lines = re.split(r"🔹", text)
        return "".join(f"<li>{line.strip()}</li>" for line in lines if line.strip())

    # Render each section in separate boxes
    st.markdown(f"""
    <div style='background-color:#e3f2fd;padding:15px;border-radius:10px;margin-bottom:15px;'>
        <h4 style='color:#0d47a1;'>🔹 Match Score</h4>
        <p style='color:#0d47a1;font-size:18px;'>{match_score_text}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background-color:#fce4ec;padding:15px;border-radius:10px;margin-bottom:15px;'>
        <h4 style='color:#880e4f;'>🔹 Missing / Weak Keywords</h4>
        <ul style='color:#880e4f;'>{format_bullets(keywords_text)}</ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background-color:#e8f5e9;padding:15px;border-radius:10px;'>
        <h4 style='color:#1b5e20;'>🔹 Suggestions to Improve Resume</h4>
        <ul style='color:#1b5e20;'>{format_bullets(suggestions_text)}</ul>
    </div>
    """, unsafe_allow_html=True)

# === Reset Button ===
if st.button("🔄 Reset"):
    for key in ['result', 'resume_text', 'jd_text']:
        st.session_state[key] = ""
    st.experimental_rerun()

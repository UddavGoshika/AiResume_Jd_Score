# ------------------- 1. IMPORT LIBRARIES -------------------
import streamlit as st
import cohere
import PyPDF2
import docx2txt
from dotenv import load_dotenv
import os
import re

# ------------------- 2. LOAD API KEY -------------------
load_dotenv()
api_key = os.getenv("API_KEY") or st.secrets.get("API_KEY")

if not api_key:
    st.error("🚨 Cohere API key not found. Please set it in a .env file or Streamlit Cloud secrets.")
    st.stop()

co = cohere.Client(api_key)

# ------------------- 3. PAGE CONFIG -------------------
st.set_page_config(page_title="Resume Matcher", page_icon="🧠", layout="centered")
st.title("🧠 AI Resume vs JD Analyzer")
st.markdown("Compare your resume with a job description and get improvement suggestions!")

# ------------------- 4. TEXT EXTRACTION -------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return ''.join([page.extract_text() or "" for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return "❌ Unsupported file type."

# ------------------- 5. AI ANALYSIS FUNCTION -------------------
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

# ------------------- 6. INPUT UI -------------------
col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_upload")
with col2:
    jd_text = st.text_area("📃 Paste Job Description Here", "", height=200)

# ------------------- 7. HTML BULLET BUILDER -------------------
def build_html_list(text):
    items = [line.strip("🔹-• \n").strip() for line in text.splitlines() if line.strip()]
    return ''.join(f"<li>{item}</li>" for item in items if item)

# ------------------- 8. ANALYZE BUTTON -------------------
if resume_file and jd_text.strip():
    st.success("✅ Inputs received. Click Analyze to proceed.")
    if st.button("🔍 Analyze"):
        with st.spinner("🔎 AI analyzing your resume..."):
            resume_text = extract_text(resume_file)
            result = analyze_resume_vs_jd(resume_text, jd_text)

        # ------------------- 9. CLEAN & EXTRACT RESPONSE -------------------
        try:
            # Normalize section headers
            result = result.replace("Missing or weak keywords:", "Missing/Weak Keywords:")
            result = result.replace("Suggestions to improve:", "Suggestions to Improve")
            result = result.replace("Suggestions to Improve Resume", "Suggestions to Improve")

            # Split sections
            parts = result.split("Missing/Weak Keywords:")
            match_score_section = parts[0].strip()
            rest = parts[1] if len(parts) > 1 else ""
            keywords_section = rest.split("Suggestions to Improve")[0].strip() if "Suggestions to Improve" in rest else ""
            suggestions_section = rest.split("Suggestions to Improve")[1].strip() if "Suggestions to Improve" in rest else ""

        except Exception as e:
            st.error(f"⚠️ Unable to parse AI response: {e}")
            st.text_area("Debug Output", result, height=300)
            st.stop()

        # Extract score (default 0 if fail)
        match = re.search(r"(\d{1,3})/100", match_score_section)
        score = int(match.group(1)) if match else 0

        # ------------------- 10. DISPLAY RESULTS -------------------
        st.subheader("📊 Match Score")
        st.progress(score / 100)

        styled_output = f"""
        <div style="background-color:#e3f2fd;padding:15px;border-radius:10px;margin-bottom:20px;">
            <h4 style="color:#0d47a1;margin-top:0;">🔹 Match Score</h4>
            <p style="font-size:18px;margin:0;">{match_score_section}</p>
        </div>

        <div style="background-color:#fce4ec;padding:15px;border-radius:10px;margin-bottom:20px;">
            <h4 style="color:#880e4f;margin-top:0;">🔹 Missing / Weak Keywords</h4>
            <ul style="margin:0;padding-left:20px;">
                {build_html_list(keywords_section)}
            </ul>
        </div>

        <div style="background-color:#e8f5e9;padding:15px;border-radius:10px;">
            <h4 style="color:#1b5e20;margin-top:0;">🔹 Suggestions to Improve Resume</h4>
            <ul style="margin:0;padding-left:20px;">
                {build_html_list(suggestions_section)}
            </ul>
        </div>
        """

        st.markdown(styled_output, unsafe_allow_html=True)

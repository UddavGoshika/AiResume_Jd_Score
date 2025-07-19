import streamlit as st
import cohere
import PyPDF2
import docx2txt
from cohere_utils import co  # Import the cohere client from your utils module
# === API KEY ===


from dotenv import load_dotenv
import os

load_dotenv() 

api_key = os.getenv("API_KEY")
if api_key:
    co = cohere.Client(api_key)
# cohere_utils.py
# Ensure you have the cohere library installed: pip install cohere  # Import the actual cohere library, not your module 



# === Text Extraction ===
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return ''.join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return "Unsupported file type."

# === Analyze with Cohere ===
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
st.set_page_config(page_title="Resume Matcher", page_icon="🧠", layout="centered")
st.title("🎯 Resume vs JD Analyzer")
st.markdown("Upload your **Resume** and **Job Description** to see how well they match!")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
with col2:
    

    jd_file = st.text_area("📃 Job Description (Paste text here)", "")

if resume_file and jd_file:
    st.success("✅ Files uploaded. Click below to analyze.")
    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing with AI..."):
            resume_text = extract_text(resume_file)
            jd_text = jd_file  # Use the text input directly
            result = analyze_resume_vs_jd(resume_text, jd_text)
        st.subheader("📊 Result")
        st.markdown(f"<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;color:#333;'>{result.replace('-', '🔹')}</div>", unsafe_allow_html=True)
import streamlit as st
import cohere
import PyPDF2
import docx2txt

# === API KEY ===
co = cohere.Client("qr4pr7IfGpLfFzm10eyUTH7UrYClOh4snS8NhBgF")  # Replace with your Cohere API key

# === Text Extraction ===
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return ''.join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        return docx2txt.process(file)
    else:
        return "Unsupported file type."

# === Analyze with Cohere ===
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
st.set_page_config(page_title="Resume Matcher", page_icon="🧠", layout="centered")
st.title("🎯 Resume vs JD Analyzer")
st.markdown("Upload your **Resume** and **Job Description** to see how well they match!")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
with col2:
    

    jd_file = st.text_area("📃 Job Description (Paste text here)", "")

if resume_file and jd_file:
    st.success("✅ Files uploaded. Click below to analyze.")
    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing with AI..."):
            resume_text = extract_text(resume_file)
            jd_text = jd_file  # Use the text input directly
            result = analyze_resume_vs_jd(resume_text, jd_text)
        st.subheader("📊 Result")
        st.markdown(f"<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;color:#333;'>{result.replace('-', '🔹')}</div>", unsafe_allow_html=True)

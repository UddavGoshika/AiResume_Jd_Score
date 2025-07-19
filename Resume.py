# app.py
import streamlit as st
from upload import get_text_from_file
from extract import extract_keywords
from analyze import analyze_keywords
from feedback import generate_feedback

st.title("📄 Resume–JD Matcher with Cohere AI")

# Upload resume
resume_file = st.file_uploader("Upload your Resume (.pdf or .docx)", type=["pdf", "docx"])
jd_text = st.text_area("Paste the Job Description (JD) here")






if resume_file and jd_text:
    with st.spinner("Processing..."):
        resume_text = get_text_from_file(resume_file)
        
        # Extract keywords
        jd_keywords = extract_keywords(jd_text, role="job")
        
        
        
        
        
        resume_keywords = extract_keywords(resume_text, role="resume")

        # Analyze
        present, missing = analyze_keywords(jd_keywords, resume_keywords)

        # Feedback
        feedback = generate_feedback(jd_keywords, present, missing)

    st.subheader("✅ JD Keywords:")
    st.write(jd_keywords)

    st.subheader("✅ Matched in Resume:")
    st.write(present)

    st.subheader("❌ Missing from Resume:")
    st.write(missing)

    st.subheader("📋 AI Feedback Report")
    st.write(feedback)

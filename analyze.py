# analyzer.py
def analyze_keywords(jd_keywords, resume_keywords):
    present = []
    missing = []

    resume_text = " ".join(resume_keywords).lower()

    for kw in jd_keywords:
        if kw.lower() in resume_text:
            present.append(kw)
        else:
            missing.append(kw)

    return present, missing

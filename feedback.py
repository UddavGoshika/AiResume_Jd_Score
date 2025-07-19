# feedback_generator.py
from cohere_utils import co

def generate_feedback(jd_keywords, present, missing):
    prompt = f"""
You're an AI resume evaluator.

JD requires: {', '.join(jd_keywords)}
Resume has: {', '.join(present)}
Missing: {', '.join(missing)}

Generate:
1. Fitment score out of 100
2. Areas to improve
3. Suggestions on how to add missing skills
"""

    response = co.generate(
        model="command-a-03-2025",
        prompt=prompt,
        max_tokens=150,
        temperature=0.4,
    )
    return response.generations[0].text.strip()

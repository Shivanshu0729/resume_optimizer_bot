import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def optimize_resume(resume_text: str, jd_text: str, missing_keywords: list) -> str:
    keywords_str = ", ".join(missing_keywords) if missing_keywords else "none identified"

    prompt = f"""You are a professional resume writer. Rewrite this resume to better match the job description.

JOB DESCRIPTION:
{jd_text}

ORIGINAL RESUME:
{resume_text}

MISSING KEYWORDS TO ADD: {keywords_str}

Rules:
1. NEVER invent jobs, companies, degrees, or dates
2. Rewrite bullet points to surface transferable skills
3. Naturally inject missing keywords where experience supports it
4. Strengthen weak bullets with action verbs (Led, Built, Optimized, Delivered)
5. Keep the same resume structure and sections
6. Return ONLY the rewritten resume text, no commentary, no markdown"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

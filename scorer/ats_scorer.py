import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def score_resume(resume_text: str, jd_text: str) -> dict:
    prompt = f"""You are a senior ATS expert. Analyze this resume against the job description.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Return ONLY valid JSON (no markdown, no backticks) in this exact format:
{{
  "total_score": <integer 0-100>,
  "keyword_score": <integer 0-100>,
  "role_alignment_score": <integer 0-100>,
  "format_score": <integer 0-100>,
  "action_verb_score": <integer 0-100>,
  "quantification_score": <integer 0-100>,
  "missing_keywords": ["keyword1", "keyword2", "keyword3"],
  "present_keywords": ["keyword1", "keyword2"],
  "gap_message": "<1-2 sentence gap explanation>",
  "is_good_match": <true if total_score >= 75 else false>,
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"]
}}

Scoring: keyword 30%, role alignment 35%, format 15%, action verbs 10%, quantification 10%.
Return ONLY the JSON, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)
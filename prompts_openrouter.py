import os
import requests
from dotenv import load_dotenv


# api_key = os.getenv("OPENROUTER_API_KEY")

import streamlit as st
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets["OPENROUTER_API_KEY"]


headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_resume_feedback(resume_text, jd_text):
    prompt = f"""
You are an expert AI career assistant.

Analyze the following RESUME and JOB DESCRIPTION.

Respond strictly in the following numbered format:

1. Skills Missing:
List 3–5 important skills mentioned in the JD that are not found in the resume.

2. Suggestions to Improve Resume:
Give 2–3 specific tips to improve the resume for this job.

3. Rewritten Resume Bullet:
Pick a weak bullet from the resume and rewrite it using numbers or measurable outcomes.

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{jd_text}
"""

    data = {
        "model": "mistralai/mistral-7b-instruct",  # or try llama3, gpt-3.5, etc.
        "messages": [
            {"role": "system", "content": "You are a helpful AI resume coach."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

    # try:
    #     response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    #     result = response.json()

    #     if "choices" in result and result["choices"]:
    #         return result["choices"][0]["message"]["content"]
    #     elif "error" in result:
    #         return f"❌ OpenRouter Error: {result['error']['message']}"
    #     else:
    #         return "❌ Unexpected API response. No feedback received."

    # except Exception as e:
    #     return f"❌ API Call Failed: {e}"


def generate_career_summary(resume_text, jd_text):
    prompt = f"""
Write a 3–4 line **professional career summary** based on the following resume and job description.

It should:
- Highlight relevant skills and experience
- Match the tone of the job description
- Sound confident and job-ready

--- RESUME ---
{resume_text}

--- JOB DESCRIPTION ---
{jd_text}
"""

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

    # try:
    #     response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    #     result = response.json()

    #     if "choices" in result and result["choices"]:
    #         return result["choices"][0]["message"]["content"]
    #     elif "error" in result:
    #         return f"❌ OpenRouter Error: {result['error']['message']}"
    #     else:
    #         return "❌ Unexpected API response. No summary generated."

    # except Exception as e:
    #     return f"❌ API Call Failed: {e}"

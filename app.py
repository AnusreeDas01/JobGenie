import json
import os
import re
import tempfile

import requests
import streamlit as st
from streamlit_lottie import st_lottie

from core.matcher import keyword_match_score
# from core.pdf_exporter import export_pdf_with_style
from core.pdf_exporter import download_report_as_html
from core.skills_loader import filter_skills_by_jd, load_skills_from_file
from jd_parser import extract_text_from_txt
from prompts_openrouter import generate_career_summary, get_resume_feedback
from resume_parser import extract_text_from_pdf


# 🧞 Lottie Genie Animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_genie = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_HpFqiS.json")
if lottie_genie:
    st_lottie(lottie_genie, height=250)

# 🧞 App Title
st.title("🧞 JobGenie: AI-Powered Resume Analyzer")

st.markdown("Upload your **resume** and a **job description** to get instant GPT-powered feedback!")
st.markdown("""
    <style>
    h1 a, h2 a, h3 a, h4 a {
        display: none !important;
    }
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput > div > div > input {
        background-color: #1c1c1c;
        color: white;
        border-radius: 8px;
    }
            
    </style>
""", unsafe_allow_html=True)


# 📤 File Upload
resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
jd_file = st.file_uploader("📃 Upload Job Description (TXT)", type=["txt"])

if resume_file and jd_file:
    with st.spinner("Analyzing your resume with AI magic... 🪄"):
        # Save temp files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_resume:
            temp_resume.write(resume_file.read())
            temp_resume_path = temp_resume.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_jd:
            temp_jd.write(jd_file.read())
            temp_jd_path = temp_jd.name

        # Extract text
        resume_text = extract_text_from_pdf(temp_resume_path).lower()
        jd_text = extract_text_from_txt(temp_jd_path).lower()

        # Load all skills from file
        skills_list = load_skills_from_file("skills.txt")

        # Filter only JD-relevant ones
        jd_skills = filter_skills_by_jd(skills_list, jd_text, threshold=85)

        # Fuzzy match resume against those JD-relevant skills
        score, matched_count, total_keywords, matched_keywords = keyword_match_score(resume_text, jd_skills, threshold=85)

        # Get missing
        missing_keywords = list(set(jd_skills) - set(matched_keywords))

        # Score + GPT feedback
        feedback = get_resume_feedback(resume_text, jd_text)
        summary = generate_career_summary(resume_text, jd_text)

        # Cleanup
        os.remove(temp_resume_path)
        os.remove(temp_jd_path)

    # ✅ Emoji Score Feedback
    st.markdown("### 📊 Match Score Result")
    if score >= 85:
        st.balloons()
        st.success(f"🔥 You're killing it! Score: {score}% ({matched_count}/{total_keywords}) matched")
    elif score >= 60:
        st.info(f"👍 Decent match: {score}% ({matched_count}/{total_keywords}) matched")
    else:
        st.warning(f"⚠️ Needs work! Score: {score}% ({matched_count}/{total_keywords}) matched")

    # ✅ Split Feedback with regex (robust fix)
    skill_gap, suggestions, rewritten = "", "", ""
    parts = re.split(r"\n?\s*\d\.\s+", feedback.strip())

    if len(parts) >= 4:
        skill_gap = parts[1].strip()
        suggestions = parts[2].strip()
        rewritten = parts[3].strip()
    else:
        st.warning("⚠️ GPT didn’t return feedback in the expected format. Try again with clearer resume + JD.")


    st.markdown("**✅ Matched Skills:**")
    st.markdown(", ".join(matched_keywords) if matched_keywords else "None")

    st.markdown("**❌ Missing Skills:**")
    st.markdown(", ".join(missing_keywords) if missing_keywords else "You're a perfect match! 🎉")

    # 💬 Output Blocks
    if skill_gap:
        st.markdown("### 🔍 Skills Missing")
        st.info(skill_gap)

    if suggestions:
        st.markdown("### ✨ Resume Improvement Suggestions")
        st.warning(suggestions)

    if rewritten:
        st.markdown("### 💡 Rewritten Resume Bullet")

        st.success(rewritten)

    # 📄 Career Summary Section
    if summary:
        st.markdown("### 📝 Career Summary Generator")
        
        st.success(summary)

    # 💾 Save Session to JSON
    session_data = {
        "resume": resume_text[:500],
        "jd": jd_text[:500],
        "score": score,
        "summary": summary,
        "feedback": feedback
    }
    with open("analysis_log.json", "w") as f:
        json.dump(session_data, f)

        # pdf_link = export_pdf_with_style(score, matched_count, total_keywords, matched_keywords, missing_keywords, summary, skill_gap, suggestions, rewritten)
        # st.markdown("### 📄 Downloadable Report")
        # st.markdown(pdf_link, unsafe_allow_html=True)
        pdf_link = download_report_as_html(
            score, matched_count, total_keywords,
            matched_keywords, missing_keywords,
            summary, skill_gap, suggestions, rewritten
        )

        st.markdown("### 📄 Downloadable Report")
        st.markdown(pdf_link, unsafe_allow_html=True)



else:
    st.info("👆 Upload both resume and job description to begin.")





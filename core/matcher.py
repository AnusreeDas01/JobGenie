# from resume_parser import extract_text_from_pdf
# from jd_parser import extract_text_from_txt
# from collections import Counter
# from rapidfuzz import fuzz
# from sklearn.feature_extraction.text import CountVectorizer

# # ✨ Use this if you want to auto-extract top keywords from JD:
# def extract_keywords_from_jd(jd_text, top_n=25):
#     vectorizer = CountVectorizer(stop_words='english', max_features=top_n)
#     X = vectorizer.fit_transform([jd_text])
#     keywords = vectorizer.get_feature_names_out().tolist()
#     return keywords

# # ✅ Clean & normalize
# def clean_text(text):
#     return text.lower().replace("\n", " ").strip()

# # ✅ Smart fuzzy keyword matcher
# def keyword_match_score(resume_text, jd_text, keywords, threshold=85):
#     resume_text = clean_text(resume_text)
#     jd_text = clean_text(jd_text)

#     matched = []
#     for keyword in keywords:
#         kw = keyword.lower()
#         # Fuzzy match with resume OR JD
#         if fuzz.partial_ratio(kw, resume_text) >= threshold or fuzz.partial_ratio(kw, jd_text) >= threshold:
#             matched.append(keyword)

#     score = round((len(matched) / len(keywords)) * 100, 2) if keywords else 0
#     return score, len(matched), len(keywords), matched

# def load_skills_from_file(file_path="skills.txt"):
#     with open(file_path, "r", encoding="utf-8") as f:
#         skills = [line.strip().lower() for line in f if line.strip()]
#     return skills



from resume_parser import extract_text_from_pdf
from jd_parser import extract_text_from_txt
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import CountVectorizer

# ✅ Load and clean skills from file
def load_skills_from_file(file_path="skills.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

# ✅ Filter skills relevant to the JD only
# def filter_skills_by_jd(skills, jd_text):
#     jd_text = jd_text.lower()
#     return [skill for skill in skills if skill in jd_text]
def filter_skills_by_jd(skills_list, jd_text, threshold=85):
    jd_text = jd_text.lower()
    relevant_skills = []
    for skill in skills_list:
        if fuzz.partial_ratio(skill, jd_text) >= threshold:
            relevant_skills.append(skill)
    return relevant_skills

# ✅ Clean plain text (normalize)
def clean_text(text):
    return text.lower().replace("\n", " ").strip()

# ✅ Fuzzy match resume against JD-relevant skills
def keyword_match_score(resume_text, keywords, threshold=90):
    resume_text = clean_text(resume_text)
    matched = []

    for kw in keywords:
        if fuzz.partial_ratio(kw, resume_text) >= threshold:
            matched.append(kw)

    score = round((len(matched) / len(keywords)) * 100, 2) if keywords else 0
    return score, len(matched), len(keywords), matched

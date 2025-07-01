def load_skills_from_file(path="skills.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def filter_skills_by_jd(all_skills, jd_text):
    return [kw for kw in all_skills if kw.lower() in jd_text.lower()]

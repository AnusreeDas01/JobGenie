def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read().strip()

# If it's also a PDF JD
from resume_parser import extract_text_from_pdf

# Test it
if __name__ == "__main__":
    jd_text = extract_text_from_txt("sample_job_description.txt")
    print("[JOB DESCRIPTION TEXT] ⬇️\n")
    print(jd_text)

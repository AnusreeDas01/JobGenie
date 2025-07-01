import pdfplumber

def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text.strip()

# Test it
if __name__ == "__main__":
    resume_text = extract_text_from_pdf("sample_resume.pdf")
    print("[RESUME EXTRACTED TEXT] ⬇️\n")
    print(resume_text)

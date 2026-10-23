
from backend.services.resume_parser import extract_resume

print("HireSense AI Resume Parser Test")

file_path = input("Enter your resume PDF/DOCX path: ").strip().strip('"')

try:
    resume_text = extract_resume(file_path)

    print("\n===== RESUME TEXT EXTRACTED =====")
    print(resume_text[:3000])

    print("\n===== PARSING SUCCESSFUL =====")

except Exception as error:
    print("\nERROR:", error)

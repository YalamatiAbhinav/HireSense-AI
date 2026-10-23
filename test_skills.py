
from backend.services.resume_parser import extract_resume
from backend.services.skill_extractor import (
    extract_skills,
    get_total_skills
)


print("===== HIRE SENSE AI SKILL ANALYZER =====")

file_path = input("Enter your resume PDF/DOCX path: ").strip().strip('"')

try:
    # Step 1: Extract resume text
    resume_text = extract_resume(file_path)

    # Step 2: Extract technical skills
    skills = extract_skills(resume_text)

    # Step 3: Display results
    print("\n===== EXTRACTED SKILLS =====")

    for category, skill_list in skills.items():
        print(f"\n{category}:")

        for skill in skill_list:
            print(f"  - {skill}")

    # Step 4: Total skills
    total = get_total_skills(skills)

    print("\n==============================")
    print("TOTAL SKILLS FOUND:", total)
    print("==============================")

except Exception as error:
    print("\nERROR:", error)

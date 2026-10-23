
from backend.services.resume_parser import extract_resume
from backend.services.resume_matcher import match_resume_with_job


job_description = """
We are hiring an AI Engineer.

Required skills:
Python, SQL, Machine Learning, Deep Learning,
Natural Language Processing, Generative AI,
Large Language Models, RAG, LangChain,
LangGraph, FastAPI, MongoDB, Git, Docker, AWS.
"""


print("===== HIRE SENSE AI RESUME MATCHER =====")

resume_path = input(
    "Enter your resume PDF/DOCX path: "
).strip().strip('"')

try:
    # Extract resume text
    resume_text = extract_resume(resume_path)

    # Compare resume with job description
    result = match_resume_with_job(
        resume_text,
        job_description
    )

    print("\n===== MATCHING RESULTS =====")

    print(
        "\nRESUME MATCH SCORE:",
        str(result["match_percentage"]) + "%"
    )

    print("\nMATCHED SKILLS:")

    for skill in result["matched_skills"]:
        print("  +", skill)

    print("\nMISSING SKILLS:")

    for skill in result["missing_skills"]:
        print("  -", skill)

    print("\nCATEGORY ANALYSIS:")

    for category, details in result["category_analysis"].items():
        print(f"\n{category}")
        print("Required:", details["required"])
        print("Matched:", details["matched"])
        print("Missing:", details["missing"])

    print("\nRECOMMENDATIONS:")

    for recommendation in result["recommendations"]:
        print("-", recommendation)

    print("\n===== MATCHING COMPLETED =====")

except Exception as error:
    print("\nERROR:", error)

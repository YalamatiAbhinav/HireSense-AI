
from backend.services.resume_parser import extract_resume
from backend.services.resume_matcher import match_resume_with_job
from backend.services.ai_recommender import (
    generate_resume_recommendations
)


job_description = """
We are hiring an AI Engineer.

Required skills:
Python, SQL, Machine Learning, Deep Learning,
Natural Language Processing, Generative AI,
Large Language Models, RAG, LangChain,
LangGraph, FastAPI, MongoDB, Git, Docker, AWS.
"""


print("===== HIRE SENSE AI RECOMMENDATION ENGINE =====")

resume_path = input(
    "Enter your resume PDF/DOCX path: "
).strip().strip('"')


try:
    # Step 1: Extract resume text
    resume_text = extract_resume(resume_path)

    # Step 2: Calculate matching score
    match_results = match_resume_with_job(
        resume_text,
        job_description
    )

    print("\nRESUME MATCH SCORE:",
          str(match_results["match_percentage"]) + "%")

    # Step 3: Generate AI recommendations
    print("\nGenerating AI recommendations...")
    print("Please wait...\n")

    recommendations = generate_resume_recommendations(
        resume_text,
        job_description,
        match_results
    )

    # Step 4: Display recommendations
    print("\n===== AI RESUME RECOMMENDATIONS =====\n")

    print(recommendations)

    print("\n===== ANALYSIS COMPLETED =====")

except Exception as error:
    print("\nERROR:", error)

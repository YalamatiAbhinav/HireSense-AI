
from backend.services.job_analyzer import analyze_job_description


job_description = """
We are looking for an AI Engineer.

Requirements:
- Strong Python programming skills.
- Knowledge of Machine Learning and Deep Learning.
- Experience with Natural Language Processing.
- Knowledge of Generative AI and Large Language Models.
- Experience building RAG applications.
- Knowledge of LangChain, LangGraph and FastAPI.
- Database knowledge including SQL and MongoDB.
- Familiarity with Git, Docker and AWS.
"""

print("===== HIRE SENSE AI JOB ANALYZER =====")

try:
    result = analyze_job_description(job_description)

    print("\nJOB DESCRIPTION ANALYSIS")

    for category, skills in result["required_skills"].items():

        print(f"\n{category}:")

        for skill in skills:
            print(" -", skill)

    print("\nTOTAL REQUIRED SKILLS:",
          result["total_required_skills"])

    print("\n===== ANALYSIS COMPLETED =====")

except Exception as error:
    print("ERROR:", error)


from backend.agents.hire_graph import run_hiresense


job_description = """
We are hiring an AI Engineer.

Required skills:
Python, SQL, Machine Learning, Deep Learning,
Natural Language Processing, Generative AI,
Large Language Models, RAG, LangChain,
LangGraph, FastAPI, MongoDB, Git, Docker, AWS.
"""


print("===== HIRE SENSE AI MULTI-AGENT SYSTEM =====")

resume_path = input(
    "Enter your resume PDF/DOCX path: "
).strip().strip('"')


try:

    print("\nStarting LangGraph workflow...")
    print("Running resume analysis...")
    print("Running job matching...")
    print("Generating recommendations...")
    print("Preparing interview questions...")

    result = run_hiresense(
        resume_path,
        job_description
    )

    if result.get("errors"):
        raise RuntimeError("; ".join(result["errors"]))

    print("\n===== FINAL ANALYSIS REPORT =====")

    print(
        "\nMATCH SCORE:",
        str(result["match_results"]["match_percentage"]) + "%"
    )

    print("\nMATCHED SKILLS:")
    print(result["match_results"]["matched_skills"])

    print("\nMISSING SKILLS:")
    print(result["match_results"]["missing_skills"])

    print("\n===== AI RECOMMENDATIONS =====")
    print(result["recommendations"])

    print("\n===== INTERVIEW PREPARATION =====")
    print(result["interview_questions"])

    print("\n===== WORKFLOW COMPLETED =====")

except Exception as error:
    print("\nERROR:", error)

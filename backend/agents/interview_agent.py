
import ollama


def interview_agent(
    resume_text: str,
    job_description: str,
    match_results: dict
) -> dict:
    """
    Generate personalized interview questions.
    """

    prompt = f"""
You are an expert technical interviewer.

Candidate Resume:
{resume_text[:5000]}

Job Description:
{job_description[:3000]}

Missing Skills:
{match_results['missing_skills']}

Generate:

1. Five technical interview questions.
2. Three questions about the candidate's projects.
3. Two behavioral interview questions.
4. Three topics the candidate should revise.

Do not invent candidate experience.
Keep questions relevant to the job.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={"temperature": 0.3}
    )

    return {
        "interview_questions": response["message"]["content"],
        "status": "Interview preparation completed"
    }

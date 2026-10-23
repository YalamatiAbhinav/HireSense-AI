
import ollama

MODEL_NAME = "llama3.2:3b"


def generate_resume_recommendations(
    resume_text: str,
    job_description: str,
    match_results: dict
) -> str:

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    prompt = f"""
You are HireSense AI, a professional resume analyst.

RESUME:
{resume_text[:5000]}

JOB DESCRIPTION:
{job_description[:3000]}

MATCH PERCENTAGE:
{match_results['match_percentage']}%

MATCHED SKILLS:
{match_results['matched_skills']}

MISSING SKILLS:
{match_results['missing_skills']}

Provide concise recommendations under these headings:

1. Overall Assessment
2. Strongest Areas
3. Important Skill Gaps
4. Five Practical Resume Improvements
5. Three Relevant Project Suggestions
6. Three Interview Preparation Tips

Rules:
- Never invent qualifications or experience.
- Be honest and specific.
- Keep recommendations relevant to the job.
- Use clear professional language.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.3,
            "num_predict": 450
        }
    )

    return response["message"]["content"]

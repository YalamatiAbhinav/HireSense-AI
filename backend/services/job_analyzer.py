
from backend.services.skill_extractor import (
    extract_skills,
    get_total_skills
)


def analyze_job_description(job_description: str) -> dict:
    """
    Extract required skills and important information
    from a job description.
    """

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    skills = extract_skills(job_description)

    return {
        "job_description": job_description.strip(),
        "required_skills": skills,
        "total_required_skills": get_total_skills(skills)
    }

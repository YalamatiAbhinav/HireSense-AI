
from backend.services.resume_matcher import match_resume_with_job


def matching_agent(
    resume_text: str,
    job_description: str
) -> dict:
    """
    Compare candidate resume with job requirements.
    """

    results = match_resume_with_job(
        resume_text,
        job_description
    )

    return {
        "match_results": results,
        "status": "Job matching completed"
    }

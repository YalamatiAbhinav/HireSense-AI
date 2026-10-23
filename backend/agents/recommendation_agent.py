
from backend.services.ai_recommender import (
    generate_resume_recommendations
)


def recommendation_agent(
    resume_text: str,
    job_description: str,
    match_results: dict
) -> dict:
    """
    Generate AI-powered resume recommendations.
    """

    recommendations = generate_resume_recommendations(
        resume_text,
        job_description,
        match_results
    )

    return {
        "recommendations": recommendations,
        "status": "Recommendations generated"
    }

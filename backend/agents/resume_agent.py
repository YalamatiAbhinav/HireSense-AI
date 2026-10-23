
from backend.services.resume_parser import extract_resume
from backend.services.skill_extractor import extract_skills


def resume_agent(resume_path: str) -> dict:
    """
    Extract resume text and identify candidate skills.
    """

    resume_text = extract_resume(resume_path)

    skills = extract_skills(resume_text)

    return {
        "resume_text": resume_text,
        "resume_skills": skills,
        "status": "Resume analysis completed"
    }

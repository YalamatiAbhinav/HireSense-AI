
from backend.services.skill_extractor import extract_skills


def match_resume_with_job(
    resume_text: str,
    job_description: str
) -> dict:

    if not resume_text.strip():
        raise ValueError("Resume cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    # Extract skills from both documents
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Flatten categorized skills into sets
    candidate_set = {
        skill.lower()
        for skills in resume_skills.values()
        for skill in skills
    }

    required_set = {
        skill.lower()
        for skills in job_skills.values()
        for skill in skills
    }

    # Find matching and missing skills
    matched = candidate_set.intersection(required_set)
    missing = required_set.difference(candidate_set)

    # Calculate match percentage
    total_required = len(required_set)

    match_percentage = (
        len(matched) / total_required * 100
        if total_required else 0
    )

    # Generate category-wise comparison
    category_analysis = {}

    for category, skills in job_skills.items():

        candidate_skills = {
            skill.lower()
            for skill in resume_skills.get(category, [])
        }

        category_required = {
            skill.lower()
            for skill in skills
        }

        category_matched = (
            category_required.intersection(candidate_skills)
        )

        category_analysis[category] = {
            "required": len(category_required),
            "matched": len(category_matched),
            "missing": sorted(
                category_required - candidate_skills
            )
        }

    # Generate recommendations
    recommendations = []

    for skill in sorted(missing):
        recommendations.append(
            f"Consider learning or gaining practical experience "
            f"in {skill}."
        )

    if not missing:
        recommendations.append(
            "All explicitly detected job skills are present. "
            "Review experience and project evidence as well."
        )

    return {
        "match_percentage": round(match_percentage, 2),
        "total_required_skills": total_required,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "category_analysis": category_analysis,
        "recommendations": recommendations
    }

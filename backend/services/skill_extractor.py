
import re


SKILL_DATABASE = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript",
        "PHP", "SQL", "R"
    ],

    "Web Technologies": [
        "HTML", "CSS", "React", "Angular", "Node.js",
        "Flask", "Django", "FastAPI"
    ],

    "Data Science": [
        "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "Scikit-learn", "Statistics", "Data Analysis",
        "Data Visualization"
    ],

    "AI and Machine Learning": [
        "Artificial Intelligence", "Machine Learning",
        "Deep Learning", "Natural Language Processing",
        "NLP", "Generative AI", "Large Language Models",
        "LLM", "RAG", "LangChain", "LangGraph",
        "Prompt Engineering", "Computer Vision",
        "Neural Networks", "Hugging Face"
    ],

    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite",
        "ChromaDB", "Redis"
    ],

    "Tools and Platforms": [
        "Git", "GitHub", "Docker", "Kubernetes",
        "VS Code", "Jupyter Notebook", "Ollama",
        "Power BI", "Tableau", "AWS", "Azure"
    ]
}


def extract_skills(resume_text: str) -> dict:
    """
    Extract skills from resume text using a skill taxonomy.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    extracted = {}

    normalized_text = re.sub(
        r"\s+",
        " ",
        resume_text.lower()
    )

    for category, skills in SKILL_DATABASE.items():

        matched_skills = []

        for skill in skills:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill.lower())
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, normalized_text):
                matched_skills.append(skill)

        if matched_skills:
            extracted[category] = matched_skills

    return extracted


def get_total_skills(extracted_skills: dict) -> int:
    """
    Return total number of unique matched skills.
    """

    return sum(
        len(skills)
        for skills in extracted_skills.values()
    )

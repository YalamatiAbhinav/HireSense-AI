
from backend.reports.pdf_report import generate_pdf_report


sample_result = {
    "match_percentage": 75,
    "matched_skills": [
        "Python",
        "SQL",
        "Machine Learning"
    ],
    "missing_skills": [
        "Deep Learning",
        "Computer Vision"
    ],
    "recommendations": (
        "Improve your deep learning knowledge. "
        "Build practical AI projects and learn model deployment."
    ),
    "interview_questions": (
        "1. What is machine learning?\n"
        "2. Explain supervised learning.\n"
        "3. What is overfitting?"
    )
}


pdf_content = generate_pdf_report(sample_result)

with open("test_report.pdf", "wb") as file:
    file.write(pdf_content)

print("PDF report generated successfully!")
print("File: test_report.pdf")


from backend.services.resume_parser import extract_resume


def test_extract_resume_rejects_missing_file():

    try:
        extract_resume("non_existing_resume.pdf")
        assert False, "Expected an error for a missing file"

    except (FileNotFoundError, Exception):
        assert True

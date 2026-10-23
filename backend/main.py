
import time
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from backend.agents.hire_graph import run_hiresense
from backend.services.resume_parser import extract_resume
from backend.services.rag_service import (
    index_resume,
    ask_resume_question,
    delete_resume_from_vector_db,
)
from backend.database.resume_db import (
    initialize_database,
    save_resume,
    get_all_resumes,
    delete_resume,
)


app = FastAPI(title="HireSense AI")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

initialize_database()


@app.get("/")
def home():
    return {"message": "HireSense AI API is running"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume."
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    file_path = UPLOAD_DIR / f"{uuid.uuid4()}{extension}"

    request_start = time.perf_counter()

    try:
        # STEP 1: Save uploaded resume
        stage_start = time.perf_counter()

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(
            f"[PERFORMANCE] File Saving: "
            f"{time.perf_counter() - stage_start:.2f} seconds",
            flush=True
        )

        # STEP 2: Extract resume text
        stage_start = time.perf_counter()

        resume_text = extract_resume(str(file_path))

        print(
            f"[PERFORMANCE] API Resume Extraction: "
            f"{time.perf_counter() - stage_start:.2f} seconds",
            flush=True
        )

        # STEP 3: Run LangGraph multi-agent workflow
        stage_start = time.perf_counter()

        result = run_hiresense(
            str(file_path),
            job_description
        )

        print(
            f"[PERFORMANCE] LangGraph Total: "
            f"{time.perf_counter() - stage_start:.2f} seconds",
            flush=True
        )

        if result.get("errors"):
            raise RuntimeError("; ".join(result["errors"]))

        # STEP 4: Index resume in ChromaDB
        stage_start = time.perf_counter()

        resume_id = index_resume(resume_text)

        print(
            f"[PERFORMANCE] ChromaDB Indexing: "
            f"{time.perf_counter() - stage_start:.2f} seconds",
            flush=True
        )

        # STEP 5: Save resume details in SQLite
        stage_start = time.perf_counter()

        save_resume(
            resume_id=resume_id,
            filename=file.filename,
            match_percentage=result["match_results"]["match_percentage"]
        )

        print(
            f"[PERFORMANCE] SQLite Saving: "
            f"{time.perf_counter() - stage_start:.2f} seconds",
            flush=True
        )

        # STEP 6: Return analysis results
        return {
            "status": "success",
            "resume_id": resume_id,
            "match_percentage": result["match_results"]["match_percentage"],
            "matched_skills": result["match_results"]["matched_skills"],
            "missing_skills": result["match_results"]["missing_skills"],
            "recommendations": result["recommendations"],
            "interview_questions": result["interview_questions"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        if file_path.exists():
            file_path.unlink()

        await file.close()

        print(
            f"[PERFORMANCE] Complete API Request: "
            f"{time.perf_counter() - request_start:.2f} seconds",
            flush=True
        )


@app.post("/chat")
def chat_with_resume(
    resume_id: str = Form(...),
    question: str = Form(...)
):
    try:
        answer = ask_resume_question(
            resume_id,
            question
        )

        return {
            "resume_id": resume_id,
            "question": question,
            "answer": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/resumes")
def list_resumes():
    try:
        return {
            "resumes": get_all_resumes()
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.delete("/resumes/{resume_id}")
def remove_resume(resume_id: str):
    try:
        delete_resume_from_vector_db(resume_id)
        delete_resume(resume_id)

        return {
            "status": "success",
            "message": "Resume deleted successfully."
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

import sys
from pathlib import Path

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
import json

import requests
import streamlit as st

from backend.reports.pdf_report import generate_pdf_report


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="HireSense AI",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# ==========================================
# SESSION STATE
# ==========================================

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "resume_id" not in st.session_state:
    st.session_state["resume_id"] = None


# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

h1 {
    color: #2563eb;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.title("🤖 HireSense AI")

st.subheader("Intelligent Resume Analyzer & Career Agent")

st.write(
    "Analyze your resume, identify skill gaps, "
    "and prepare for your dream job using local AI."
)

st.divider()


# ==========================================
# BACKEND STATUS
# ==========================================

# ==========================================
# BACKEND STATUS
# ==========================================

try:
    health = requests.get(
        f"{API_URL}/",
        timeout=5
    )

    if health.status_code == 200:
        st.success("HireSense AI Backend Connected")
    else:
        st.warning("Backend is not responding correctly.")

except requests.RequestException:
    st.error(
        "Backend is offline. Start FastAPI in another terminal."
    )



# ==========================================
# RESUME UPLOAD
# ==========================================

st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)


# ==========================================
# JOB DESCRIPTION
# ==========================================

st.header("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=220,
    placeholder="Paste the complete job description..."
)


# ==========================================
# ANALYZE RESUME
# ==========================================

if st.button("🚀 Analyze My Resume"):

    if uploaded_file is None:
        st.warning("Please upload your resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        with st.spinner(
            "HireSense AI is analyzing your resume. Please wait..."
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                data = {
                    "job_description": job_description
                }

                response = requests.post(
                    f"{API_URL}/analyze",
                    files=files,
                    data=data,
                    timeout=600
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state["analysis_result"] = result

                    st.session_state["resume_id"] = result.get(
                        "resume_id"
                    )

                    st.session_state["chat_history"] = []

                    st.success("Resume analysis completed!")

                else:

                    try:
                        error_message = response.json().get(
                            "detail",
                            response.text
                        )
                    except ValueError:
                        error_message = response.text

                    st.error(f"Analysis failed: {error_message}")

            except requests.Timeout:

                st.error(
                    "The analysis took too long. Please try again."
                )

            except requests.RequestException as error:

                st.error(f"Connection error: {error}")


# ==========================================
# DISPLAY ANALYSIS RESULTS
# ==========================================

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]

    st.divider()

    st.header("📊 Resume Analysis Report")

    score = result.get("match_percentage", 0)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Resume Match Score",
            f"{score}%"
        )

    with col2:
        st.metric(
            "Matched Skills",
            len(result.get("matched_skills", []))
        )

    st.progress(
        max(0.0, min(float(score) / 100, 1.0))
    )

    # Matched skills
    st.subheader("✅ Matched Skills")

    matched = result.get("matched_skills", [])

    if matched:
        st.write(", ".join(map(str, matched)))
    else:
        st.info("No matched skills found.")

    # Missing skills
    st.subheader("❌ Missing Skills")

    missing = result.get("missing_skills", [])

    if missing:
        st.write(", ".join(map(str, missing)))
    else:
        st.success("No missing skills reported.")

    # Recommendations
    st.subheader("🧠 AI Recommendations")

    st.markdown(
        result.get(
            "recommendations",
            "No recommendations available."
        )
    )

    # Interview preparation
    st.subheader("🎯 Interview Preparation")

    st.markdown(
        result.get(
            "interview_questions",
            "No interview questions available."
        )
    )

    st.divider()

    # PDF download
    st.subheader("📥 Download Reports")

    try:

        pdf_file = generate_pdf_report(result)

        st.download_button(
            label="📄 Download Resume Analysis PDF",
            data=pdf_file,
            file_name="HireSense_AI_Report.pdf",
            mime="application/pdf"
        )

    except Exception as error:
        st.error(f"PDF generation failed: {error}")

    # JSON download
    st.download_button(
        label="Download Analysis as JSON",
        data=json.dumps(result, indent=4),
        file_name="hiresense_analysis.json",
        mime="application/json"
    )


# ==========================================
# CHAT WITH YOUR RESUME
# ==========================================

if st.session_state.get("resume_id"):

    st.divider()

    st.header("💬 Chat with Your Resume")

    st.write("Ask questions about your uploaded resume.")

    st.caption("Suggested questions:")

    suggested_questions = [
        "What are my technical skills?",
        "What projects are mentioned in my resume?",
        "What certifications do I have?",
        "What are my strongest skills?",
        "What experience do I have?"
    ]

    # Display previous chat messages
    for message in st.session_state["chat_history"]:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Suggested question buttons
    question = None

    columns = st.columns(2)

    for index, suggested in enumerate(suggested_questions):

        with columns[index % 2]:

            if st.button(
                suggested,
                key=f"suggest_{index}"
            ):
                question = suggested

    # Only ONE chat input in the application
    chat_input = st.chat_input(
        "Ask anything about your resume...",
        key="resume_chat_input"
    )

    if chat_input:
        question = chat_input

    # Process the selected question
    if question:

        st.session_state["chat_history"].append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing your resume..."):

                try:

                    response = requests.post(
                        f"{API_URL}/chat",
                        data={
                            "resume_id": st.session_state["resume_id"],
                            "question": question
                        },
                        timeout=180
                    )

                    if response.status_code == 200:

                        answer = response.json()["answer"]

                    else:

                        answer = f"Error: {response.text}"

                except requests.RequestException as error:

                    answer = f"Connection error: {error}"

                st.markdown(answer)

        st.session_state["chat_history"].append({
            "role": "assistant",
            "content": answer
        })


# ==========================================
# RESUME HISTORY
# ==========================================

st.divider()

st.header("📁 Resume History")

try:

    response = requests.get(
        f"{API_URL}/resumes",
        timeout=30
    )

    if response.status_code == 200:

        history_data = response.json()
        resumes = history_data.get("resumes", [])

        if resumes:

            st.success(
                f"Total saved resumes: {len(resumes)}"
            )

            # Select a resume for chatting
            resume_options = {
                (
                    f'{resume["filename"]} | '
                    f'{resume["match_percentage"]}% | '
                    f'{resume["uploaded_at"]}'
                ): resume["resume_id"]
                for resume in resumes
            }

            selected_resume = st.selectbox(
                "Select a resume",
                options=list(resume_options.keys())
            )

            if st.button("Use Selected Resume"):

                selected_resume_id = resume_options[selected_resume]

                st.session_state["resume_id"] = selected_resume_id

                st.session_state["chat_history"] = []

                st.success(
                    "Selected resume is ready for chatting!"
                )

                st.rerun()

            st.divider()

            # Display and delete saved resumes
            for resume in resumes:

                with st.expander(resume["filename"]):

                    st.write(
                        "Resume ID:",
                        resume["resume_id"]
                    )

                    st.write(
                        "Match Score:",
                        f'{resume["match_percentage"]}%'
                    )

                    st.write(
                        "Uploaded At:",
                        resume["uploaded_at"]
                    )

                    # Delete confirmation belongs INSIDE the loop
                    confirm_delete = st.checkbox(
                        "I want to delete this resume",
                        key=f'confirm_delete_{resume["resume_id"]}'
                    )

                    if st.button(
                        "🗑️ Delete Resume",
                        key=f'delete_{resume["resume_id"]}',
                        disabled=not confirm_delete
                    ):

                        try:

                            delete_response = requests.delete(
                                f'{API_URL}/resumes/{resume["resume_id"]}',
                                timeout=30
                            )

                            if delete_response.status_code == 200:

                                st.success(
                                    "Resume deleted successfully!"
                                )

                                # Clear selected resume if deleted
                                if (
                                    st.session_state.get("resume_id")
                                    == resume["resume_id"]
                                ):

                                    st.session_state["resume_id"] = None
                                    st.session_state["chat_history"] = []

                                # Clear analysis display if necessary
                                if "analysis_result" in st.session_state:
                                    if (
                                        st.session_state["analysis_result"].get(
                                            "resume_id"
                                        ) == resume["resume_id"]
                                    ):
                                        del st.session_state["analysis_result"]

                                st.rerun()

                            else:

                                st.error(
                                    f"Delete failed: {delete_response.text}"
                                )

                        except requests.RequestException as error:

                            st.error(
                                f"Connection error: {error}"
                            )

        else:

            st.info("No resumes found in history.")

    else:

        st.error(
            f"Could not load resume history: {response.text}"
        )

except requests.RequestException as error:

    st.error(
        f"Connection error while loading resume history: {error}"
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "HireSense AI | Powered by Python, FastAPI, "
    "LangGraph, ChromaDB and Ollama"
)

# HireSense AI – Intelligent Resume Analysis Agent

HireSense AI is an AI-powered resume analysis application that evaluates resumes against job descriptions, identifies matching and missing skills, generates recommendations, and prepares interview questions.

The application uses locally running AI models through Ollama, a LangGraph-based agent workflow, and Retrieval-Augmented Generation (RAG) to answer questions about uploaded resumes.

## Features

- **Resume Parsing:** Extracts information from PDF and DOCX resumes.
- **Job Matching:** Compares resume skills with job description requirements.
- **Skill Gap Analysis:** Identifies matched and missing skills.
- **AI Recommendations:** Generates recommendations based on resume analysis.
- **Interview Preparation:** Generates relevant interview questions.
- **Resume Chatbot:** Answers questions about uploaded resumes using RAG.
- **Resume History:** Stores and manages previously analyzed resumes.
- **Report Generation:** Downloads analysis results in PDF and JSON formats.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Models | Ollama |
| Agent Workflow | LangGraph |
| Vector Database | ChromaDB |
| Database | SQLite |
| Resume Parsing | PyMuPDF, python-docx |
| Testing | Pytest |

## Project Architecture

1. User uploads a resume and enters a job description through Streamlit.
2. FastAPI receives the request.
3. Resume parsing extracts the resume text.
4. LangGraph coordinates the resume analysis agents.
5. The matching agent compares resume skills with job requirements.
6. The recommendation and interview agents generate their respective outputs.
7. ChromaDB stores resume chunks for semantic retrieval.
8. Ollama runs the local language and embedding models.
9. SQLite stores resume history.
10. Streamlit displays the results and provides report downloads.

## Project Structure

```text
HireSense-AI/
├── backend/
│   ├── agents/
│   ├── services/
│   ├── schemas/
│   ├── database/
│   ├── reports/
│   └── main.py
├── frontend/
│   └── app.py
├── data/
│   ├── uploads/
│   └── chroma_db/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

- Python 3.10 or later
- Ollama installed
- Git (optional)

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd HireSense-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Download Ollama models

Install Ollama, then run:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Make sure the Ollama service is running.

## Running the Application

Open two terminals from the project root.

**Terminal 1 – Backend**

```bash
uvicorn backend.main:app --reload
```

**Terminal 2 – Frontend**

```bash
streamlit run frontend/app.py
```

Open the local Streamlit URL displayed in the terminal.

## Running Tests

```bash
python -m pytest tests -v
```

## Privacy and Local Execution

HireSense AI uses locally running Ollama models for AI processing. Resume files, SQLite data, and ChromaDB storage are maintained locally by the application. Do not upload private resumes or local database files to a public repository.

## Project Goal

This project demonstrates practical implementation of AI agents, LLM integration, RAG, vector databases, API development, document processing, and full-stack AI application development.
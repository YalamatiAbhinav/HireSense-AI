
import sqlite3
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "data" / "hiresense.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id TEXT UNIQUE NOT NULL,
            filename TEXT NOT NULL,
            match_percentage REAL,
            uploaded_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_resume(resume_id, filename, match_percentage):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO resumes (
            resume_id,
            filename,
            match_percentage,
            uploaded_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        resume_id,
        filename,
        match_percentage,
        datetime.now().isoformat(timespec="seconds")
    ))

    connection.commit()
    connection.close()



def get_all_resumes():

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT resume_id, filename, match_percentage, uploaded_at
        FROM resumes
        ORDER BY id DESC
    """)

    resumes = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return resumes


def delete_resume(resume_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM resumes WHERE resume_id = ?",
        (resume_id,)
    )

    deleted_count = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted_count > 0
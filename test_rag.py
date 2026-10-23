
from backend.services.resume_parser import extract_resume

from backend.services.rag_service import (
    index_resume,
    ask_resume_question
)


print("===== HIRE SENSE AI RAG CHATBOT =====")

resume_path = input(
    "Enter your resume PDF/DOCX path: "
).strip().strip('"')


try:

    # Step 1: Extract resume text
    resume_text = extract_resume(resume_path)

    print("\nResume extracted successfully.")

    # Step 2: Index resume into ChromaDB
    print("\nCreating resume embeddings...")

    resume_id = index_resume(resume_text)

    print("Resume indexed successfully!")

    print("\nResume ID:", resume_id)

    # Step 3: Start chatbot
    print("\n===== CHATBOT STARTED =====")
    print("Type 'exit' to stop the chatbot.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("\nChatbot closed.")
            break

        if not question:
            print("Please enter a question.")
            continue

        answer = ask_resume_question(
            resume_id,
            question
        )

        print("\nHireSense AI:", answer)


except Exception as error:

    print("\nERROR:", error)

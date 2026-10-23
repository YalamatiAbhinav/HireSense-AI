
import ollama

print("Connecting to HireSense AI...")

try:
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": "You are HireSense AI. Explain how AI can analyze a resume in 3 simple points."
            }
        ]
    )

    print("\n===== HIRE SENSE AI RESPONSE =====")
    print(response["message"]["content"])
    print("\n===== TEST COMPLETED SUCCESSFULLY =====")

except Exception as e:
    print("\nERROR:", e)
    print("Check whether Ollama is running and the model is downloaded.")

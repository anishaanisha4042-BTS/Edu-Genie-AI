import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

client = genai.Client(api_key=API_KEY)


def answer_question(question: str) -> str:
    prompt = f"""
You are an educational AI assistant.

Answer the following question clearly and accurately.
Use simple language suitable for students.

Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error while generating answer: {str(e)}"
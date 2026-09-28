import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)


def summarize_text(text: str) -> str:
    if not API_KEY:
        return "Gemini API key is missing. Please add GEMINI_API_KEY to your .env file."

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""
Summarize the following text for a student.

Make the summary:
- concise
- simple
- easy to understand
- useful for quick revision

Text:
{text}
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error while summarizing: {str(e)}"
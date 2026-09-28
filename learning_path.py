import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a personalized learning path for the topic: {topic}

Organize it into three levels:

1. Beginner
2. Intermediate
3. Advanced

For each level:
- List important concepts to learn.
- Suggest useful resources such as videos, articles, or books.
- Keep the explanation simple and student-friendly.

Return the learning path in a clear and organized format.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating learning path: {str(e)}"
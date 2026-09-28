import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

client = genai.Client(api_key=API_KEY)


def clean_json_block(text: str) -> str:
    """Remove Markdown code fences if Gemini returns them."""
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_quiz(topic: str) -> str:
    prompt = f"""
You are an educational quiz generator.

Create exactly 3 multiple-choice questions about:

{topic}

Requirements:
- Exactly 3 questions
- Each question must have exactly 4 options
- Only one option must be correct
- Make the wrong options plausible
- Keep the questions suitable for students
- Include the correct answer
- Return ONLY valid JSON
- Do not add explanations outside the JSON

Use this exact JSON format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A"
  }},
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option B"
  }},
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option C"
  }}
]
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        result = response.text

        if not result:
            return "Gemini returned an empty response."

        result = clean_json_block(result)

        quiz_data = json.loads(result)

        if not isinstance(quiz_data, list):
            return "Invalid quiz format returned by Gemini."

        if len(quiz_data) != 3:
            return "Gemini did not generate exactly 3 questions."

        for question in quiz_data:
            if "question" not in question:
                return "Invalid question format."

            if "options" not in question:
                return "Invalid options format."

            if "answer" not in question:
                return "Invalid answer format."

            if len(question["options"]) != 4:
                return "Each question must have exactly 4 options."

        return json.dumps(quiz_data, indent=2, ensure_ascii=False)

    except json.JSONDecodeError:
        return "Gemini returned invalid JSON. Please try again."

    except Exception as e:
        return f"Error while generating quiz: {str(e)}"
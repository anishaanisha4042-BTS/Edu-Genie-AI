from transformers import pipeline


_explainer = None


def get_explainer():
    global _explainer

    if _explainer is None:
        _explainer = pipeline(
            "text2text-generation",
            model="MBZUAI/LaMini-Flan-T5-783M"
        )

    return _explainer


def explain_concept(concept: str) -> str:
    try:
        explainer = get_explainer()

        prompt = f"""
Explain the following concept in very simple language
for a beginner student.

Concept:
{concept}

Use a short and easy explanation with a simple example if possible.
"""

        result = explainer(
            prompt,
            max_new_tokens=180,
            do_sample=False
        )

        return result[0]["generated_text"]

    except Exception as e:
        return f"Error while explaining the concept: {str(e)}"
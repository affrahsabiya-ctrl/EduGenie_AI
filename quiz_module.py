import json

from gemini_client import generate_text


def generate_quiz(text: str) -> dict:
    """
    Generate a 5-question multiple-choice quiz.
    """

    text = text.strip()

    if not text:
        raise ValueError(
            "Study material cannot be empty."
        )

    prompt = f"""
Create a 5-question multiple-choice quiz
from the following study material.

Study material:
{text}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "title": "Quiz",
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": 0,
      "explanation": "Why the answer is correct"
    }}
  ]
}}

Rules:
- Create exactly 5 questions.
- Each question must have exactly 4 options.
- "answer" must be 0, 1, 2, or 3.
- The answer index must match the correct option.
- Questions must be based only on the supplied material.
- Do not use Markdown.
- Return JSON only.
"""

    result = generate_text(
        prompt,
        system_instruction=(
            "You are an educational quiz generator. "
            "When JSON is requested, return valid JSON only."
        ),
        temperature=0.2,
        max_output_tokens=2500,
    )

    return _parse_quiz_response(result)


def _parse_quiz_response(result: str) -> dict:
    """
    Safely parse and validate Gemini's quiz JSON.
    """

    cleaned = result.strip()

    # Remove Markdown code fences if Gemini adds them.
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    try:
        quiz = json.loads(cleaned)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid quiz JSON."
        ) from exc

    if not isinstance(quiz, dict):
        raise ValueError(
            "Quiz response must be a JSON object."
        )

    questions = quiz.get("questions")

    if not isinstance(questions, list):
        raise ValueError(
            "Quiz response does not contain questions."
        )

    valid_questions = []

    for question in questions:

        if not isinstance(question, dict):
            continue

        question_text = question.get(
            "question"
        )

        options = question.get(
            "options"
        )

        answer = question.get(
            "answer"
        )

        explanation = question.get(
            "explanation",
            "",
        )

        if not question_text:
            continue

        if not isinstance(options, list):
            continue

        if len(options) != 4:
            continue

        if not isinstance(answer, int):
            continue

        if answer < 0 or answer > 3:
            continue

        valid_questions.append(
            {
                "question": str(
                    question_text
                ),
                "options": [
                    str(option)
                    for option in options
                ],
                "answer": answer,
                "explanation": str(
                    explanation
                ),
            }
        )

    if not valid_questions:
        raise ValueError(
            "No valid quiz questions were generated."
        )

    return {
        "title": str(
            quiz.get(
                "title",
                "EduGenie Quiz",
            )
        ),
        "questions": valid_questions,
    }
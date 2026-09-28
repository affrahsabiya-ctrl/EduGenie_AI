from gemini_client import generate_text


def get_learning_recommendations(subject: str) -> str:
    """
    Generate a structured learning path for a subject.
    """

    prompt = f"""
Create a structured learning path for a student who wants to learn:

{subject}

Organize the learning path into:

1. Beginner
2. Intermediate
3. Advanced

For each level include:
- Topics to learn
- Skills to develop
- Practice activities
- One suggested project

Also include:
- Recommended learning order
- A realistic weekly study plan
- General resource types to use

Requirements:
- Start with fundamentals.
- Each level should build on the previous level.
- Keep the recommendations practical.
- Use clear student-friendly language.
- Do not invent specific courses, websites, or links.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are an experienced learning-path designer. "
            "Create practical and progressive study plans "
            "for students."
        ),
        temperature=0.4,
        max_output_tokens=1800,
    )
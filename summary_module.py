from gemini_client import generate_text


def summarize_text(text: str) -> str:
    """
    Create concise revision notes from educational text.
    """

    prompt = f"""
Summarize the following educational material for a student.

Study material:
{text}

Create useful revision notes.

Include these sections:

1. Main Idea
2. Key Points
3. Important Terms
4. Quick Revision

Requirements:
- Preserve the important information from the source.
- Do not invent facts.
- Use clear and simple language.
- Use bullet points where appropriate.
- Keep the summary significantly shorter than the original.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are an educational summarization assistant. "
            "Create accurate and easy-to-revise study notes."
        ),
        temperature=0.3,
        max_output_tokens=1400,
    )
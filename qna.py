def answer_question(question: str) -> str:
    """
    Answer a student's educational question.
    """

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    # Local answers for common questions
    answers = {
        "what is photosynthesis?": """
Photosynthesis is the process by which green plants prepare their own food using sunlight, carbon dioxide, and water.

Main points:
- It mainly takes place in the leaves.
- Chlorophyll absorbs sunlight.
- Plants take in carbon dioxide from the air.
- Roots absorb water from the soil.
- Glucose is produced as food.
- Oxygen is released into the atmosphere.

Example:
A green plant uses sunlight, water, and carbon dioxide to prepare its food.

In simple words:
Photosynthesis = Sunlight + Water + Carbon Dioxide → Food + Oxygen.
""",

        "what is python?": """
Python is a high-level, interpreted programming language.

Main points:
- Python has simple and readable syntax.
- It is easy for beginners to learn.
- It supports many libraries and frameworks.
- It is used in web development, AI, automation, and data science.

Example:
print("Hello World")

In simple words:
Python is a simple and powerful programming language.
""",

        "what is a computer?": """
A computer is an electronic device that accepts data, processes it, stores it, and produces useful information.

Main parts:
- Input devices enter data.
- CPU processes the data.
- Memory stores data.
- Output devices display the result.

Example:
A keyboard is used to enter data and a monitor displays the result.

In simple words:
Computer = Input → Processing → Output → Storage.
"""
    }

    key = question.lower()

    if key in answers:
        return answers[key]

    # Generic local answer
    return f"""
Your question is: {question}

This is an educational question that can be understood by studying its basic definition, important points, and examples.

Key Points:
- Understand the basic meaning of the concept.
- Learn its important features.
- Study a simple practical example.
- Revise the main points for better understanding.

Example:
Try connecting the concept with a real-life situation to understand it more easily.

Note:
For detailed AI-generated answers, Gemini API access is required.
"""
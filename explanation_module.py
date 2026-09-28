def explain_topic(topic: str) -> str:
    """
    Explain an educational topic in a simple student-friendly way.
    """

    topic = topic.strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    explanations = {
        "photosynthesis": """
1. Definition

Photosynthesis is the process by which green plants prepare their own food using sunlight, carbon dioxide, and water.

2. Key Ideas

- It mainly takes place in the leaves of green plants.
- Chlorophyll absorbs sunlight.
- Carbon dioxide enters through tiny openings called stomata.
- Water is absorbed by the roots.
- Glucose is produced as food.
- Oxygen is released into the atmosphere.

3. Simple Example

A green plant kept in sunlight uses water from the soil and carbon dioxide from the air to prepare food.

4. Memory Tip

Remember: Sunlight + Water + Carbon Dioxide → Food + Oxygen.
""",

        "python": """
1. Definition

Python is a high-level, interpreted programming language used to develop software, websites, automation tools, and AI applications.

2. Key Ideas

- Python has simple and readable syntax.
- It supports object-oriented programming.
- It provides many useful libraries.
- Python is widely used in Artificial Intelligence and Data Science.

3. Simple Example

A simple Python program can print a message:

print("Hello World")

4. Memory Tip

Remember: Python = Simple Syntax + Powerful Libraries + Many Applications.
""",

        "computer": """
1. Definition

A computer is an electronic device that accepts data, processes it, stores it, and produces useful information.

2. Key Ideas

- Input devices are used to enter data.
- The CPU processes the data.
- Memory stores data and instructions.
- Output devices display the result.

3. Simple Example

When we type a question using a keyboard, the computer processes it and displays the result on the screen.

4. Memory Tip

Remember: Input → Process → Output → Storage.
"""
    }

    key = topic.lower()

    if key in explanations:
        return explanations[key]

    return f"""
1. Definition

{topic} is an important educational concept that can be understood by studying its basic meaning, features, and applications.

2. Key Ideas

- Understand the basic meaning of {topic}.
- Learn its important features.
- Study how it is used in practical situations.
- Remember the main points using simple examples.

3. Simple Example

A simple example related to {topic} can be studied to understand the concept more clearly.

4. Memory Tip

Remember the definition, key ideas, example, and practical use of {topic}.
"""
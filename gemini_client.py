import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.8-flash"

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add your Gemini API key to the .env file."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
) -> str:

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    config = {
        "max_output_tokens": max_output_tokens,
    }

    if system_instruction:
        config["system_instruction"] = system_instruction

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=config,
            )
            break

        except Exception as exc:
            if attempt == 2:
                raise exc

            time.sleep(5)

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title="EduGenie AI",
    description=(
        "AI-powered educational assistant for "
        "Q&A, explanations, quizzes, summaries, "
        "and personalized learning paths."
    ),
    version="1.0.0",
)


# ============================================================
# Static files and templates
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ============================================================
# Request models
# ============================================================

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class ExplanationRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000,
    )


# ============================================================
# Helper
# ============================================================

def clean_input(value: str) -> str:
    """
    Remove unnecessary whitespace.
    """
    return value.strip()


# ============================================================
# Frontend
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


# ============================================================
# Health check
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie AI",
        "version": "1.0.0",
    }


# ============================================================
# Q&A
# ============================================================

@app.post("/qa")
async def qa(request: QuestionRequest):

    question = clean_input(
        request.question
    )

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        answer = answer_question(
            question
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        print(
            f"Q&A error: {exc}"
        )

        raise HTTPException(
            status_code=500,
           detail=f"Q&A error: {exc}",
        ) from exc


# ============================================================
# Explanation
# ============================================================

@app.post("/explain")
async def explain(
    request: ExplanationRequest
):

    topic = clean_input(
        request.topic
    )

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Topic cannot be empty.",
        )

    try:

        explanation = explain_topic(
            topic
        )

        return {
            "explanation": explanation
        }

    except Exception as exc:

        print(
            f"Explanation error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate the explanation. "
                "Please check your Gemini API configuration."
            ),
        ) from exc


# ============================================================
# Quiz
# ============================================================

@app.post("/quiz")
async def quiz(
    request: TextRequest
):

    text = clean_input(
        request.text
    )

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Study material cannot be empty.",
        )

    try:

        quiz_data = generate_quiz(
            text
        )

        return quiz_data

    except Exception as exc:

        print(
            f"Quiz error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate the quiz. "
                "Please check your Gemini API configuration."
            ),
        ) from exc


# ============================================================
# Summarization
# ============================================================

@app.post("/summarize")
async def summarize(
    request: TextRequest
):

    text = clean_input(
        request.text
    )

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    try:

        summary = summarize_text(
            text
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        print(
            f"Summary error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to summarize the text. "
                "Please check your Gemini API configuration."
            ),
        ) from exc


# ============================================================
# Learning path
# ============================================================

@app.post(
    "/learn/recommendations"
)
async def learning_recommendations(
    request: TextRequest
):

    subject = clean_input(
        request.text
    )

    if not subject:
        raise HTTPException(
            status_code=400,
            detail="Subject cannot be empty.",
        )

    try:

        recommendations = (
            get_learning_recommendations(
                subject
            )
        )

        return {
            "recommendations": recommendations
        }

    except Exception as exc:

        print(
            f"Learning path error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to create the learning path. "
                "Please check your Gemini API configuration."
            ),
        ) from exc


# ============================================================
# Local development entry point
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
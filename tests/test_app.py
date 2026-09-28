from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


@patch(
    "main.answer_question",
    return_value="The Pacific Ocean is the largest ocean."
)
def test_qa_endpoint(mock_answer):
    response = client.post(
        "/qa",
        json={
            "question": "Which is the largest ocean?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "Pacific" in data["answer"]

    mock_answer.assert_called_once()


@patch(
    "main.explain_topic",
    return_value="The Pythagorean theorem relates the sides of a right triangle."
)
def test_explanation_endpoint(mock_explain):
    response = client.post(
        "/explain",
        json={
            "topic": "Pythagorean theorem"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "explanation" in data
    assert "Pythagorean" in data["explanation"]

    mock_explain.assert_called_once()


@patch(
    "main.generate_quiz",
    return_value={
        "title": "Photosynthesis Quiz",
        "questions": [
            {
                "question": "What do plants use to make food?",
                "options": [
                    "Light energy",
                    "Sound",
                    "Plastic",
                    "Metal",
                ],
                "answer": 0,
                "explanation": "Plants use light energy during photosynthesis.",
            }
        ],
    },
)
def test_quiz_endpoint(mock_quiz):
    response = client.post(
        "/quiz",
        json={
            "text": "Photosynthesis uses light energy."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "questions" in data
    assert len(data["questions"]) == 1

    mock_quiz.assert_called_once()


@patch(
    "main.summarize_text",
    return_value="Photosynthesis is how plants convert light energy into chemical energy."
)
def test_summary_endpoint(mock_summary):
    response = client.post(
        "/summarize",
        json={
            "text": "Photosynthesis is the process by which plants convert light energy into chemical energy."
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "Photosynthesis" in data["summary"]

    mock_summary.assert_called_once()


@patch(
    "main.get_learning_recommendations",
    return_value="Beginner: Learn SQL basics."
)
def test_learning_path_endpoint(mock_learning):
    response = client.post(
        "/learn/recommendations",
        json={
            "text": "SQL"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "recommendations" in data
    assert "SQL" in data["recommendations"]

    mock_learning.assert_called_once()
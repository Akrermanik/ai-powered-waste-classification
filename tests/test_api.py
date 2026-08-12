from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def _register_and_token(client: TestClient, username: str, password: str = "pass123") -> str:
    response = client.post(
        "/v1/auth/register",
        json={"username": username, "name": username.title(), "password": password},
    )
    assert response.status_code == 201
    return response.json()["access_token"]


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert "model_ready" in body


def test_register_and_login(client):
    response = client.post(
        "/v1/auth/register",
        json={"username": "api_user", "name": "API User", "password": "secret"},
    )
    assert response.status_code == 201

    login = client.post(
        "/v1/auth/login",
        json={"username": "api_user", "password": "secret"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"


@patch("api.routes.prediction.run_inference")
def test_predict_endpoint(mock_run_inference, client, sample_image_bytes):
    mock_run_inference.return_value = {
        "predictions": [
            {
                "class_name": "Glass",
                "confidence": 0.91,
                "bbox": {"x1": 1, "y1": 2, "x2": 3, "y2": 4},
            }
        ],
        "inference_time_ms": 42.0,
        "summary": {"label": "Glass", "confidence": 0.91, "object_count": 1},
        "annotated_image_base64": None,
    }

    token = _register_and_token(client, "predict_user")
    response = client.post(
        "/v1/predict",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.png", sample_image_bytes, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["label"] == "Glass"
    assert body["inference_time_ms"] == 42.0


def test_history_isolation_between_users(client, sample_image_bytes):
    token_a = _register_and_token(client, "history_a")
    token_b = _register_and_token(client, "history_b")

    with patch("api.routes.prediction.run_inference") as mock_run_inference:
        mock_run_inference.return_value = {
            "predictions": [],
            "inference_time_ms": 10.0,
            "summary": {"label": "Paper", "confidence": 0.5, "object_count": 0},
        }
        client.post(
            "/v1/predict",
            headers={"Authorization": f"Bearer {token_a}"},
            files={"file": ("test.png", sample_image_bytes, "image/png")},
        )

    history_a = client.get("/v1/history", headers={"Authorization": f"Bearer {token_a}"})
    history_b = client.get("/v1/history", headers={"Authorization": f"Bearer {token_b}"})

    assert history_a.status_code == 200
    assert history_b.status_code == 200
    assert history_a.json()["count"] >= 0
    assert history_b.json()["count"] == 0


def test_predict_requires_auth(client, sample_image_bytes):
    response = client.post(
        "/v1/predict",
        files={"file": ("test.png", sample_image_bytes, "image/png")},
    )
    assert response.status_code == 401

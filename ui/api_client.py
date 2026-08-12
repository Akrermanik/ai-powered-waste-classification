"""HTTP client for Streamlit to communicate with the FastAPI backend."""

from __future__ import annotations

import io
from typing import Any

import httpx
from PIL import Image

from core.config import API_BASE_URL


class APIClientError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class WasifyAPIClient:
    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or API_BASE_URL).rstrip("/")
        self.token = token

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def health(self) -> dict[str, Any]:
        response = httpx.get(f"{self.base_url}/health", timeout=30.0)
        response.raise_for_status()
        return response.json()

    def register(self, username: str, name: str, password: str) -> dict[str, Any]:
        response = httpx.post(
            f"{self.base_url}/v1/auth/register",
            json={"username": username, "name": name, "password": password},
            timeout=30.0,
        )
        if response.status_code >= 400:
            detail = response.json().get("detail", "Registration failed")
            raise APIClientError(detail, response.status_code)
        return response.json()

    def login(self, username: str, password: str) -> dict[str, Any]:
        response = httpx.post(
            f"{self.base_url}/v1/auth/login",
            json={"username": username, "password": password},
            timeout=30.0,
        )
        if response.status_code >= 400:
            detail = response.json().get("detail", "Login failed")
            raise APIClientError(detail, response.status_code)
        return response.json()

    def predict(self, image: Image.Image, confidence: float = 0.5) -> dict[str, Any]:
        if not self.token:
            raise APIClientError("Authentication required", 401)

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        response = httpx.post(
            f"{self.base_url}/v1/predict",
            headers=self._headers(),
            files={"file": ("image.png", buffer.getvalue(), "image/png")},
            params={"confidence": confidence},
            timeout=120.0,
        )
        if response.status_code >= 400:
            detail = response.json().get("detail", "Prediction failed")
            raise APIClientError(detail, response.status_code)
        return response.json()

    def get_history(self, limit: int = 50) -> dict[str, Any]:
        if not self.token:
            raise APIClientError("Authentication required", 401)

        response = httpx.get(
            f"{self.base_url}/v1/history",
            headers=self._headers(),
            params={"limit": limit},
            timeout=30.0,
        )
        if response.status_code >= 400:
            detail = response.json().get("detail", "Failed to load history")
            raise APIClientError(detail, response.status_code)
        return response.json()

    def delete_history_item(self, prediction_id: int) -> None:
        if not self.token:
            raise APIClientError("Authentication required", 401)

        response = httpx.delete(
            f"{self.base_url}/v1/history/{prediction_id}",
            headers=self._headers(),
            timeout=30.0,
        )
        if response.status_code >= 400:
            detail = response.json().get("detail", "Failed to delete prediction")
            raise APIClientError(detail, response.status_code)

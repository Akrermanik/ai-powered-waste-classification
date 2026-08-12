# Wasify Architecture

## Overview

Wasify is an API-driven waste classification platform. The frontend and backend are separated so the same REST API can serve the Streamlit UI, automated tests, and future clients.

```text
User
 ↓
Streamlit (frontend)
 ↓ HTTP / REST
FastAPI (backend)
 ↓
core/inference.py
 ↓
YOLO11 (waste_model.pt)
 ↓
Prediction result
 ↓
SQLite (user-specific history)
```

## Frontend — Streamlit

- Entry point: `app.py`
- UI modules: `ui/dashboard.py`, `ui/auth_pages.py`, `ui/styles.py`
- Communicates with FastAPI via `ui/api_client.py`
- Handles presentation only: image upload, camera capture, result display, history view

Streamlit does **not** run YOLO inference or write directly to the database for predictions.

## Backend — FastAPI

- Entry point: `api/main.py`
- Run locally: `uvicorn api.main:app --reload`
- Routes:
  - `GET /health`
  - `POST /v1/auth/register`
  - `POST /v1/auth/login`
  - `POST /v1/predict`
  - `GET /v1/history`
  - `GET /v1/history/{prediction_id}`
  - `DELETE /v1/history/{prediction_id}`

## ML — YOLO11

- Centralized in `core/inference.py`
- Loads `waste_model.pt` (configurable via `MODEL_PATH`)
- Returns structured predictions with bounding boxes, confidence scores, and optional annotated image (base64)

Both FastAPI and any legacy helpers import from this module — inference is not duplicated.

## Database — SQLite

- Connection and schema: `database/connection.py`
- User operations: `database/users.py`
- Prediction operations: `database/predictions.py`

### Tables

**users**

| Column | Type |
| ------ | ---- |
| id | INTEGER PK |
| username | TEXT UNIQUE |
| name | TEXT |
| password_hash | TEXT |
| created_at | TEXT |

**predictions**

| Column | Type |
| ------ | ---- |
| id | INTEGER PK |
| user_id | INTEGER FK → users.id |
| timestamp | TEXT |
| label | TEXT |
| confidence | REAL |
| object_count | INTEGER |
| inference_time_ms | REAL |
| bbox_json | TEXT (JSON array of detections) |

> SQLite is suitable for demo and single-instance deployment. A production multi-instance deployment would use PostgreSQL or another server-based database with connection pooling.

## Authentication

- Service: `auth/service.py`
- Passwords hashed with bcrypt (never stored in plaintext)
- JWT tokens issued on register/login (`WASIFY_AUTH_SECRET` required)
- Protected API routes require `Authorization: Bearer <token>`
- Each user sees only their own prediction history

## Configuration

Environment variables (see `.env.example`):

| Variable | Purpose |
| -------- | ------- |
| WASIFY_AUTH_SECRET | JWT signing key and legacy cookie secret |
| ROBOFLOW_API_KEY | Dataset download (training only) |
| DATABASE_URL | SQLite file path |
| API_BASE_URL | FastAPI URL for Streamlit client |
| MODEL_PATH | Path to YOLO weights |

## Testing & CI

- Tests: `tests/` (pytest)
- Lint: Ruff (`ruff check .`)
- CI: `.github/workflows/ci.yml` runs tests and lint on push/PR

## Why This Separation?

- **Reusability**: Mobile apps, scripts, or other frontends can call the same API.
- **Testability**: API and business logic are tested without Streamlit.
- **Interview clarity**: Demonstrates REST API design, auth, database layering, and ML serving as distinct concerns.

## Legacy Code

- `archive/v1_react_native/` — old mobile app
- `utils/Model.py` — deprecated FastAPI stub using `yolov8n.pt` (do not use)

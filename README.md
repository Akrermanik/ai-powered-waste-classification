# Wasify — AI-Powered Waste Classification (Full-Stack Architecture)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-wasteclassification.streamlit.app/)

An intelligent waste classification system built with a **FastAPI backend**, an interactive **Streamlit frontend**, and a custom-trained **YOLO11 object detection model**. The system enables users to upload or capture images and automatically identify waste items in real time, providing annotated detections, confidence scores, and waste category information.

This project has been fully upgraded to a modern, decoupled, API-driven architecture to demonstrate robust software engineering principles.

---

## 🚀 Live Demo

The frontend is live and ready to use!

**[👉 Access the App Here: https://ai-wasteclassification.streamlit.app/](https://ai-wasteclassification.streamlit.app/)**

---

## 🏗️ Architecture Overview

This system is built using a modern decoupled architecture:

*   **Frontend (Streamlit):** A lightweight, interactive UI that communicates exclusively via REST API calls. (No heavy ML libraries loaded on the client).
*   **Backend (FastAPI):** A high-performance, stateless API layer that handles user authentication, history storage, and orchestrates YOLO inference.
*   **Inference Engine (YOLO11 / PyTorch):** A centralized `core/inference.py` service that processes image tensors and returns structured JSON predictions.
*   **Database (SQLite):** A relational database storing user credentials (securely hashed with `bcrypt`) and a chronological history of user predictions.

```text
┌───────────────┐        REST API         ┌────────────────┐
│               │   (JSON / form-data)    │                │
│   Streamlit   │────────────────────────▶│    FastAPI     │
│   Frontend    │                         │    Backend     │
│               │◀────────────────────────│                │
└───────────────┘       Responses         └───────┬────────┘
                                                  │
                                                  ▼
                                          ┌────────────────┐
                                          │  YOLO11 Model  │
                                          │ (Inference Core)│
                                          └────────────────┘
```

---

## 📊 Model Performance

The custom YOLO11 model is trained to detect 13 different waste classes (Plastic, Paper, Organic, Metal, E-Waste, etc.).

*   **Dataset Size**: 46,204 total annotated images.
*   **mAP@50**: 0.630
*   **Precision (P)**: 0.646
*   **Recall (R)**: 0.630
*   **Inference Latency (CPU)**: ~114 ms per image

---

## 💻 Running Locally

### 1. Clone & Setup
```bash
git clone <repository-url>
cd ai-powered-waste-classification
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 2. Install Dependencies
Because of the decoupled architecture, the backend requires the heavy ML libraries, while the frontend only requires lightweight HTTP clients.

```bash
# Install backend dependencies (FastAPI, YOLO, PyTorch)
pip install -r requirements-backend.txt

# Install frontend dependencies (Streamlit, httpx)
pip install -r requirements.txt
```

### 3. Start the Backend Server (Terminal 1)
```bash
uvicorn api.main:app --reload
# API Documentation will be live at http://localhost:8000/docs
```

### 4. Start the Frontend App (Terminal 2)
```bash
streamlit run app.py
# App will be live at http://localhost:8501
```

---

## 🚢 Deployment

This repository is configured for effortless cloud deployment using two separate platforms:

1.  **Backend (Render):** Uses the included `Dockerfile` and `render.yaml` to spin up a background worker for FastAPI.
2.  **Frontend (Streamlit Cloud):** Uses `requirements.txt` (which is stripped of PyTorch/YOLO to prevent OOM errors) and points to the Render backend via the `API_BASE_URL` secret.

### Docker Support
You can also run the entire stack locally in one click using Docker Compose:
```bash
docker-compose up --build
```

---

## 🧪 Testing & CI/CD
The project features a comprehensive test suite testing both the API routes and the inference engine mocks. 
```bash
# Run the test suite
pytest

# Enforce code quality
ruff check .
```
A GitHub Actions workflow (`ci.yml`) automatically runs these tests on every push.

---
## 📝 License
This project is open-source and available under the MIT License.

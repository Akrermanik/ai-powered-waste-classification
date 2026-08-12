"""Application configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project root (parent of core/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Security
AUTH_SECRET = os.getenv("WASIFY_AUTH_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("WASIFY_JWT_EXPIRE_MINUTES", "1440"))

# External services
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY", "")

# Database
DATABASE_PATH = os.getenv(
    "DATABASE_URL",
    str(PROJECT_ROOT / "wasify.db"),
).replace("sqlite:///", "")

# Model
MODEL_PATH = os.getenv("MODEL_PATH", str(PROJECT_ROOT / "models" / "waste_model.pt"))
DEFAULT_CONFIDENCE = float(os.getenv("DEFAULT_CONFIDENCE", "0.5"))

# API
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

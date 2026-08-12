from fastapi import APIRouter

from core.inference import is_model_ready

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "model_ready": is_model_ready(),
    }

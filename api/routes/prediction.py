import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from api.dependencies import get_current_user
from api.schemas.prediction import PredictionItem, PredictionSummary, PredictResponse
from core.config import DEFAULT_CONFIDENCE
from core.history import save_prediction
from core.inference import run_inference

router = APIRouter(prefix="/v1", tags=["prediction"])


@router.post("/predict", response_model=PredictResponse)
async def predict_waste(
    file: UploadFile = File(...),
    confidence: float = DEFAULT_CONFIDENCE,
    current_user: dict = Depends(get_current_user),
) -> PredictResponse:
    if file.filename is None or file.content_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid image file is required",
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Upload a JPEG, PNG, or WebP image.",
        )

    contents = await file.read()
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file",
        ) from exc

    try:
        result = run_inference(
            image,
            confidence_threshold=confidence,
            include_annotated_image=True,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Inference failed",
        ) from exc

    summary = result["summary"]
    prediction_id = save_prediction(
        user_id=current_user["id"],
        label=summary["label"],
        confidence=summary["confidence"],
        object_count=summary["object_count"],
        inference_time_ms=result["inference_time_ms"],
        predictions=result["predictions"],
    )

    return PredictResponse(
        predictions=[PredictionItem(**item) for item in result["predictions"]],
        inference_time_ms=result["inference_time_ms"],
        summary=PredictionSummary(**summary),
        prediction_id=prediction_id,
        annotated_image_base64=result.get("annotated_image_base64"),
    )

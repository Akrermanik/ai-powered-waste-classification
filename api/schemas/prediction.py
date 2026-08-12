from pydantic import BaseModel


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class PredictionItem(BaseModel):
    class_name: str
    confidence: float
    bbox: BoundingBox


class PredictionSummary(BaseModel):
    label: str
    confidence: float
    object_count: int


class PredictResponse(BaseModel):
    predictions: list[PredictionItem]
    inference_time_ms: float
    summary: PredictionSummary
    prediction_id: int | None = None
    annotated_image_base64: str | None = None

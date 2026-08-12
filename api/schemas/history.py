from pydantic import BaseModel


class HistoryItem(BaseModel):
    id: int
    user_id: int
    timestamp: str
    label: str
    confidence: float
    object_count: int | None = None
    inference_time_ms: float | None = None
    predictions: list[dict] = []


class HistoryListResponse(BaseModel):
    items: list[HistoryItem]
    count: int

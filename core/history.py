"""Prediction history business logic."""

from database.predictions import (
    delete_prediction,
    get_prediction_by_id,
    get_predictions_for_user,
    insert_prediction,
)


def save_prediction(
    user_id: int,
    label: str,
    confidence: float,
    object_count: int | None = None,
    inference_time_ms: float | None = None,
    predictions: list | None = None,
) -> int:
    return insert_prediction(
        user_id=user_id,
        label=label,
        confidence=confidence,
        object_count=object_count,
        inference_time_ms=inference_time_ms,
        predictions=predictions,
    )


def list_user_history(user_id: int, limit: int = 50) -> list[dict]:
    return get_predictions_for_user(user_id, limit=limit)


def get_user_prediction(user_id: int, prediction_id: int) -> dict | None:
    return get_prediction_by_id(prediction_id, user_id)


def remove_user_prediction(user_id: int, prediction_id: int) -> bool:
    return delete_prediction(prediction_id, user_id)

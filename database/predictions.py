"""Prediction history database operations."""

import json

from database.connection import get_connection, init_db


def insert_prediction(
    user_id: int,
    label: str,
    confidence: float,
    object_count: int | None = None,
    inference_time_ms: float | None = None,
    predictions: list | None = None,
) -> int:
    init_db()
    bbox_json = json.dumps(predictions) if predictions else None
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO predictions
                (user_id, label, confidence, object_count, inference_time_ms, bbox_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, label, confidence, object_count, inference_time_ms, bbox_json),
        )
        conn.commit()
        return int(cursor.lastrowid)
    finally:
        conn.close()


def get_predictions_for_user(user_id: int, limit: int = 50) -> list[dict]:
    init_db()
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, user_id, timestamp, label, confidence, object_count,
                   inference_time_ms, bbox_json
            FROM predictions
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    finally:
        conn.close()

    results = []
    for row in rows:
        item = dict(row)
        if item.get("bbox_json"):
            item["predictions"] = json.loads(item["bbox_json"])
        else:
            item["predictions"] = []
        del item["bbox_json"]
        results.append(item)
    return results


def get_prediction_by_id(prediction_id: int, user_id: int) -> dict | None:
    init_db()
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT id, user_id, timestamp, label, confidence, object_count,
                   inference_time_ms, bbox_json
            FROM predictions
            WHERE id = ? AND user_id = ?
            """,
            (prediction_id, user_id),
        ).fetchone()
    finally:
        conn.close()

    if not row:
        return None

    item = dict(row)
    item["predictions"] = json.loads(item["bbox_json"]) if item.get("bbox_json") else []
    del item["bbox_json"]
    return item


def delete_prediction(prediction_id: int, user_id: int) -> bool:
    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM predictions WHERE id = ? AND user_id = ?",
            (prediction_id, user_id),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

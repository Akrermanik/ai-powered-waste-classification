"""Centralized YOLO11 inference service for Wasify."""

from __future__ import annotations

import base64
import io
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO

from core.config import DEFAULT_CONFIDENCE, MODEL_PATH

_model: YOLO | None = None
_model_loaded: bool = False


def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_model(model_path: str | None = None) -> YOLO | None:
    """Load the Wasify YOLO model. Returns None if weights are missing."""
    global _model, _model_loaded

    path = Path(model_path or MODEL_PATH)
    if not path.exists():
        _model = None
        _model_loaded = False
        return None

    if _model is None or str(path) != getattr(_model, "_wasify_path", ""):
        _model = YOLO(str(path))
        _model._wasify_path = str(path)  # type: ignore[attr-defined]
        device = get_device()
        if device in ("cuda", "mps"):
            _model.to(device)
        _model_loaded = True

    return _model


def is_model_ready() -> bool:
    return load_model() is not None


def _parse_boxes(result: Any, confidence_threshold: float) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []
    if result.boxes is None or len(result.boxes) == 0:
        return predictions

    for conf, cls, box in zip(result.boxes.conf, result.boxes.cls, result.boxes.xyxy):
        confidence = float(conf.item())
        if confidence < confidence_threshold:
            continue
        x1, y1, x2, y2 = (float(v) for v in box.tolist())
        class_id = int(cls.item())
        class_name = result.names[class_id]
        predictions.append(
            {
                "class_name": class_name,
                "confidence": confidence,
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            }
        )

    predictions.sort(key=lambda item: item["confidence"], reverse=True)
    return predictions


def _build_summary(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    if not predictions:
        return {
            "label": "No Objects Detected",
            "confidence": 0.0,
            "object_count": 0,
        }

    classes = list(dict.fromkeys(p["class_name"] for p in predictions))
    return {
        "label": ", ".join(classes),
        "confidence": max(p["confidence"] for p in predictions),
        "object_count": len(predictions),
    }


def _encode_image_rgb(image_rgb: np.ndarray) -> str:
    pil_image = Image.fromarray(image_rgb.astype(np.uint8))
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def run_inference(
    image: Image.Image,
    confidence_threshold: float = DEFAULT_CONFIDENCE,
    include_annotated_image: bool = False,
) -> dict[str, Any]:
    """
    Run YOLO inference on a PIL image.

    Returns structured predictions suitable for API responses.
    """
    model = load_model()
    if model is None:
        raise FileNotFoundError(
            f"Model weights not found at {MODEL_PATH}. "
            "Train the model and place waste_model.pt in the project root."
        )

    device = get_device()
    start = time.perf_counter()
    results = model.predict(image, device=device, conf=confidence_threshold)
    inference_time_ms = round((time.perf_counter() - start) * 1000, 2)

    result = results[0]
    predictions = _parse_boxes(result, confidence_threshold)
    summary = _build_summary(predictions)

    output: dict[str, Any] = {
        "predictions": predictions,
        "inference_time_ms": inference_time_ms,
        "summary": summary,
    }

    if include_annotated_image:
        annotated_bgr = result.plot()
        annotated_rgb = annotated_bgr[:, :, ::-1]
        output["annotated_image_base64"] = _encode_image_rgb(annotated_rgb)

    return output


def predict_waste(image: Image.Image, confidence_threshold: float = DEFAULT_CONFIDENCE):
    """
    Backward-compatible helper used by legacy code paths.

    Returns: annotated_img_rgb, label_name, top_conf, object_count, inference_time_ms
    """
    result = run_inference(
        image,
        confidence_threshold=confidence_threshold,
        include_annotated_image=True,
    )
    summary = result["summary"]

    if "annotated_image_base64" in result:
        import base64 as b64

        image_bytes = b64.b64decode(result["annotated_image_base64"])
        annotated_img_rgb = np.array(Image.open(io.BytesIO(image_bytes)))
    else:
        annotated_img_rgb = np.array(image.convert("RGB"))

    return (
        annotated_img_rgb,
        summary["label"],
        summary["confidence"],
        summary["object_count"],
        int(result["inference_time_ms"]),
    )

from unittest.mock import MagicMock, patch

import numpy as np

from core.inference import _build_summary, _parse_boxes, run_inference


class FakeBox:
    def __init__(self, conf, cls, xyxy):
        self.conf = [MagicMock(item=lambda: conf)]
        self.cls = [MagicMock(item=lambda: cls)]
        self.xyxy = [MagicMock(tolist=lambda: xyxy)]


class FakeBoxes:
    def __init__(self, boxes):
        self.conf = [b.conf[0] for b in boxes]
        self.cls = [b.cls[0] for b in boxes]
        self.xyxy = [b.xyxy[0] for b in boxes]
        
    def __len__(self):
        return len(self.conf)

class FakeResult:
    def __init__(self, boxes=None, names=None):
        self.boxes = FakeBoxes(boxes) if boxes else None
        self.names = names or {0: "Plastic_Bottle"}

    def plot(self):
        return np.zeros((64, 64, 3), dtype=np.uint8)


def test_build_summary_empty():
    summary = _build_summary([])
    assert summary["label"] == "No Objects Detected"
    assert summary["confidence"] == 0.0
    assert summary["object_count"] == 0


def test_build_summary_with_predictions():
    predictions = [
        {"class_name": "Glass", "confidence": 0.8, "bbox": {}},
        {"class_name": "Plastic_Bottle", "confidence": 0.9, "bbox": {}},
    ]
    summary = _build_summary(predictions)
    assert "Glass" in summary["label"]
    assert summary["confidence"] == 0.9
    assert summary["object_count"] == 2


def test_parse_boxes_filters_by_threshold():
    boxes = [FakeBox(0.9, 0, [1, 2, 3, 4]), FakeBox(0.2, 0, [5, 6, 7, 8])]
    result = FakeResult(boxes=boxes, names={0: "Paper"})
    parsed = _parse_boxes(result, confidence_threshold=0.5)
    assert len(parsed) == 1
    assert parsed[0]["class_name"] == "Paper"
    assert parsed[0]["confidence"] == 0.9


@patch("core.inference.load_model")
def test_run_inference_returns_structured_data(mock_load_model, sample_image):
    fake_model = MagicMock()
    fake_result = FakeResult(
        boxes=[FakeBox(0.95, 0, [10, 20, 30, 40])],
        names={0: "Metal"},
    )
    fake_model.predict.return_value = [fake_result]
    mock_load_model.return_value = fake_model

    output = run_inference(sample_image, confidence_threshold=0.5)

    assert output["summary"]["label"] == "Metal"
    assert output["summary"]["object_count"] == 1
    assert len(output["predictions"]) == 1
    assert "inference_time_ms" in output


@patch("core.inference.load_model", return_value=None)
def test_run_inference_missing_model(mock_load_model, sample_image):
    try:
        run_inference(sample_image)
        raised = False
    except FileNotFoundError:
        raised = True
    assert raised

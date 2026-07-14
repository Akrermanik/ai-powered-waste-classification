import os
import time
import torch
from ultralytics import YOLO

model_path = "waste_model.pt"
model = None
if os.path.exists(model_path):
    model = YOLO(model_path)
    if torch.backends.mps.is_available():
        model.to("mps")

def predict_waste(image, confidence_threshold):
    if model is None:
        raise ValueError("Model is not loaded. Please make sure waste_model.pt exists.")

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    start_time = time.perf_counter()
    results = model.predict(image, device=device, conf=confidence_threshold)
    inference_time_ms = int((time.perf_counter() - start_time) * 1000)
    result = results[0]

    annotated_img_bgr = result.plot()
    annotated_img_rgb = annotated_img_bgr[:, :, ::-1]

    if len(result.boxes) > 0:
        detected_classes = []
        confidences = []
        for conf, cls in zip(result.boxes.conf, result.boxes.cls):
            detected_classes.append(result.names[int(cls.item())])
            confidences.append(float(conf.item()))

        top_conf = max(confidences)
        label_name = ", ".join(list(set(detected_classes)))
        object_count = len(result.boxes)
    else:
        top_conf = 0.0
        label_name = "No Objects Detected"
        object_count = 0

    return annotated_img_rgb, label_name, top_conf, object_count, inference_time_ms
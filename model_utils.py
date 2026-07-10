import cv2
import os
import time
import torch
from ultralytics import YOLO

# Initialize YOLO model globally
model_path = 'waste_model.pt'
model = None
if os.path.exists(model_path):
    model = YOLO(model_path)
    if torch.backends.mps.is_available():
        model.to("mps")

def predict_waste(image, confidence_threshold):
    """
    Runs YOLO inference on the input image.
    Returns:
        annotated_img_rgb (np.array): The image with drawn bounding boxes.
        label_name (str): The predicted class name.
        top_conf (float): The confidence score.
        object_count (int): The number of detected objects.
        inference_time_ms (int): The inference time in milliseconds.
    """
    if model is None:
        raise ValueError("Model is not loaded. Please make sure waste_model.pt exists.")

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    start_time = time.perf_counter()
    results = model.predict(image, device=device, conf=confidence_threshold)
    inference_time_ms = int((time.perf_counter() - start_time) * 1000)
    result = results[0]

    annotated_img_bgr = result.plot()
    annotated_img_rgb = cv2.cvtColor(annotated_img_bgr, cv2.COLOR_BGR2RGB)

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

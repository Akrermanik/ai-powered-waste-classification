from pathlib import Path

from ultralytics import YOLO

# Resume or start training from a checkpoint in the local runs/ directory.
checkpoint = Path("runs/detect/runs/waste_yolo11_m4_optimized/weights/last.pt")
if checkpoint.exists():
    model = YOLO(str(checkpoint))
    model.train(resume=True)
else:
    model = YOLO("yolo11n.pt")
    model.train(
        data="waste-dataset-v5-prev-1/data.yaml",
        epochs=50,
        imgsz=640,
        batch=8,
        workers=2,
        cache=False,
        device="cpu",
        project="runs",
        name="waste_yolo11_m4_optimized",
        exist_ok=True,
        patience=10,
    )

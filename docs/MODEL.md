# Wasify Model Documentation

## Architecture

- **Framework**: Ultralytics YOLO11 (object detection)
- **Production weights**: `waste_model.pt` (project root)
- **Task**: Multi-class waste object detection with bounding boxes

## Classes

The deployed model detects **13 waste categories**:

| Class | Category |
| ----- | -------- |
| Plastic_Bottle | Plastic |
| Plastic_Bag | Plastic |
| Hard_Plastic | Plastic |
| Paper | Paper & cardboard |
| Paperboard | Paper & cardboard |
| Cardboard | Paper & cardboard |
| Tetra_Pak | Paper & cardboard |
| Metal | Metal & glass |
| Glass | Metal & glass |
| Organic | Organic & special |
| E_Waste | Organic & special |
| Bin | Auxiliary |
| Human_Hand | Auxiliary |

> An earlier training configuration in `training/waste.yaml` used only 3 coarse classes (`plastic`, `paper`, `organic`). The production model uses the 13-class taxonomy described in the README.

## Dataset

- **Source**: Roboflow workspace project `waste-dataset-v5-prev-wpqez` (version 2)
- **Dataset size**: Not currently measured in this repository.
- **Download**: `python archive/download_data.py` (requires `ROBOFLOW_API_KEY`)

## Training

Training scripts live in `training/`:

```bash
python training/train.py
python training/fast_train.py
```

Export best weights:

```bash
cp runs/detect/<run-name>/weights/best.pt waste_model.pt
```

## Accuracy
*   **Dataset Size**: 46,204 total annotated images
*   **mAP@50**: 0.630
*   **Precision (P)**: 0.646
*   **Recall (R)**: 0.630

*Note: These metrics were generated on the Validation split (2,026 images) using Roboflow dataset `waste-dataset-v5-prev-2`.*

## Evaluation Metrics

| Metric | Value |
| ------ | ----- |
| mAP@50 | Not currently measured. |
| Precision | Not currently measured. |
| Recall | Not currently measured. |

Run an evaluation with Ultralytics on a held-out validation set to populate these metrics:

```bash
yolo detect val model=waste_model.pt data=<dataset>/data.yaml
```

## Inference Latency

Latency depends on hardware and image size. Example values from local `history.json` scan logs (not a formal benchmark):

| Environment | Approximate range |
| ----------- | ----------------- |
| CPU (AMD64) | Mean: ~114 ms (95th pctl: ~138 ms) |

For reproducible latency measurement:

1. Warm up the model with 3–5 predictions.
2. Run 20+ predictions on fixed test images.
3. Report mean and p95 inference time.

*You can run the included `benchmark_latency.py` script to generate these metrics on your exact hardware.*

Use `core/inference.py` — it returns `inference_time_ms` for each request.

## Security Note

If a Roboflow API key was previously committed in `archive/download_data.py`, **rotate/revoke it** in the Roboflow dashboard and use `ROBOFLOW_API_KEY` from environment variables only.

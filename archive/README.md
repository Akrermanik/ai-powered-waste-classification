# Legacy Code Archive

This directory contains legacy and experimental code that is **not** part of the current production architecture.

## Contents

- `v1_react_native/` — Legacy React Native mobile app (V1). Superseded by the Streamlit + FastAPI web application.
- `download_data.py` — Roboflow dataset download utility (requires `ROBOFLOW_API_KEY` env var).
- `debug_roboflow.py` — Roboflow connectivity check script.

## Current Production Architecture

The current application uses:

```text
Streamlit (frontend) → FastAPI (backend) → YOLO11 inference + SQLite
```

Do not use files in `utils/Model.py` (old FastAPI server using `yolov8n.pt`) for production. Use `api/main.py` instead.

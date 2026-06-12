# AI-Powered Waste Classification

An intelligent waste classification system built using a custom-trained **YOLO11 object detection model** and an interactive **Streamlit web application**. The system enables users to upload or capture images and automatically identify waste items in real time, providing annotated detections, confidence scores, and waste category information.

Designed to support sustainable waste management and recycling initiatives, the application leverages modern computer vision techniques to automate waste segregation across multiple waste categories.

---

## Overview

Waste segregation is a critical step in effective recycling and environmental sustainability. This project uses deep learning-based object detection to identify and classify waste materials directly from images.

Unlike traditional image classification systems, the model performs **object detection**, allowing it to locate and classify multiple waste items within a single image while displaying bounding boxes and confidence scores for each detection.

---

## Key Features

### Computer Vision

* Real-time waste detection using a fine-tuned YOLO11 model
* Multi-object detection within a single image
* Detection across 13 waste categories
* Bounding box visualization
* Confidence score reporting
* Custom-trained waste dataset support

### User Experience

* Image upload support
* Live camera capture
* Interactive Streamlit dashboard
* Adjustable confidence threshold
* Instant classification results

### Data Management

* User registration and login system
* Session management and authentication
* SQLite-based user storage
* Classification history tracking
* Local persistence of the most recent scans

---

## System Workflow

```text
┌─────────────────┐
│   User Image    │
│ Upload / Camera │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ YOLO11 Detector │
│ waste_model.pt  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Object Detection│
│ & Classification│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Annotated Image │
│ Confidence Data │
│ Detection Logs  │
└─────────────────┘
```

### Detection Pipeline

1. User logs into the application.
2. An image is uploaded or captured using the camera.
3. The image is processed by the YOLO11 model.
4. Waste objects are detected and classified.
5. Confidence scores and bounding boxes are generated.
6. Results are displayed in the dashboard and saved to history.

---

## Supported Waste Categories

The deployed model is trained to detect **13 different waste classes**.

### Plastic Waste

| Class          | Description                                |
| -------------- | ------------------------------------------ |
| Plastic_Bottle | Single-use and reusable plastic bottles    |
| Plastic_Bag    | Shopping bags, wrappers, and soft plastics |
| Hard_Plastic   | Rigid containers and plastic packaging     |

### Paper & Cardboard

| Class      | Description                             |
| ---------- | --------------------------------------- |
| Paper      | Documents, newspapers, and paper waste  |
| Paperboard | Cartons and lightweight board packaging |
| Cardboard  | Corrugated cardboard boxes              |
| Tetra_Pak  | Juice cartons and milk cartons          |

### Metal & Glass

| Class | Description                      |
| ----- | -------------------------------- |
| Metal | Cans, foil, and metal containers |
| Glass | Bottles, jars, and glass waste   |

### Organic & Special Waste

| Class   | Description                                            |
| ------- | ------------------------------------------------------ |
| Organic | Food scraps and biodegradable waste                    |
| E_Waste | Batteries, cables, chargers, and electronic components |

### Auxiliary Classes

| Class      | Description                                                                       |
| ---------- | --------------------------------------------------------------------------------- |
| Bin        | Waste bins and collection containers                                              |
| Human_Hand | Hand appearing in the image frame, used as contextual information during training |

> **Note:** The current production model uses a 13-class waste taxonomy. An earlier training configuration contained only three coarse categories (`plastic`, `paper`, and `organic`).

---

## Technology Stack

### Machine Learning & Computer Vision

* PyTorch
* Ultralytics YOLO11
* OpenCV
* Pillow (PIL)
* Roboflow

### Web Application

* Streamlit
* streamlit-authenticator
* SQLite

### Backend & Utilities

* Python
* FastAPI (optional inference API)
* JSON-based local history storage

---

## Project Structure

```text
ai-powered-waste-classification/
│
├── app.py                  # Streamlit application entry point
├── auth.py                 # Authentication configuration
├── database.py             # SQLite database utilities
├── model_utils.py          # YOLO inference logic
├── train.py                # Model training script
├── fast_train.py           # Optimized training configuration
├── download_data.py        # Dataset download utility
├── waste.yaml              # Dataset configuration
├── waste_model.pt          # Trained model weights
├── history.json            # Classification history
├── requirements.txt
│
└── utils/
    ├── Model.py            # Optional FastAPI inference server
    └── ...
```

---

## Prerequisites

Before running the project, ensure the following are installed:

### Requirements

* Python 3.9 or higher
* pip
* Trained model file (`waste_model.pt`)

### Recommended for Training

* CUDA-enabled GPU or Apple Silicon device
* Roboflow API key

---

# Getting Started

## 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-powered-waste-classification
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Launch the Application

```bash
streamlit run app.py
```

The application will start at:

```text
http://localhost:8501
```

---

## Using the Application

1. Register a new account.
2. Log in using your credentials.
3. Upload an image or capture one using the camera.
4. Adjust the confidence threshold if needed.
5. Click **Analyze**.
6. View the detected waste objects, confidence scores, and annotated image.
7. Access previous scans through the history section.

---

## Model Training

### Download the Dataset

```bash
python download_data.py
```

A valid Roboflow API key is required.

### Train the Model

```bash
python train.py
```

Training outputs are stored under:

```text
runs/
```

### Export Best Weights

```bash
cp runs/detect/<run-name>/weights/best.pt waste_model.pt
```

### Faster Training Configuration

```bash
python fast_train.py
```

---

## Configuration

| File           | Purpose                             |
| -------------- | ----------------------------------- |
| waste.yaml     | Dataset paths and class definitions |
| waste_model.pt | Production model weights            |
| history.json   | Classification history              |
| wasify.db      | SQLite user database                |
| .env           | Optional environment variables      |

---

## Future Enhancements

* Real-time video stream detection
* Recycling recommendations


---


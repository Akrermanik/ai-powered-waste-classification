# AI-Powered Waste Classification

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-wasteclassification.streamlit.app/)

An intelligent waste classification system built using a custom-trained **YOLO11 object detection model** and an interactive **Streamlit web application**. The system enables users to upload or capture images and automatically identify waste items in real time, providing annotated detections, confidence scores, and waste category information.

Designed to support sustainable waste management and recycling initiatives, the application leverages modern computer vision techniques to automate waste segregation across multiple waste categories.

---

## 🚀 Quick Start - Live Demo

The application is **live and ready to use** on Streamlit Community Cloud:

**[👉 Access the App Here: https://ai-wasteclassification.streamlit.app/](https://ai-wasteclassification.streamlit.app/)**

### Using the Live App

1. Visit the link above
2. Create a new account or log in
3. Upload an image or capture one with your camera
4. Adjust the confidence threshold if needed
5. Click **Analyze** to get instant waste classification results
6. View detection history in your dashboard

No installation required! The app is ready to use in your browser.

---

## Overview

Waste segregation is a critical step in effective recycling and environmental sustainability. This project uses deep learning-based object detection to identify and classify waste materials directly from images.

Unlike traditional image classification systems, the model performs **object detection**, allowing it to locate and classify multiple waste items within a single image while displaying bounding boxes and confidence scores for each detection.

---

## Key Features

### 🤖 Computer Vision

* Real-time waste detection using a fine-tuned YOLO11 model
* Multi-object detection within a single image
* Detection across 13 waste categories
* Bounding box visualization
* Confidence score reporting
* Custom-trained waste dataset support

### 🎨 User Experience

* Image upload support
* Live camera capture (browser-based)
* Interactive Streamlit dashboard
* Adjustable confidence threshold
* Instant classification results
* Real-time annotation overlay

### 🔐 Authentication & Data Management

* User registration and login system
* Secure session management
* SQLite-based user storage
* Classification history tracking
* Local persistence of recent scans
* Privacy-focused data handling

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

## 🌐 Using the Deployed Application (Recommended for Users)

The easiest way to use this application is through the live Streamlit deployment:

**[👉 https://ai-wasteclassification.streamlit.app/](https://ai-wasteclassification.streamlit.app/)**

Simply visit the link, create an account, and start classifying waste. No installation or setup required.

---

## 💻 Running Locally (For Development & Training)

If you want to run the application locally or train your own model, follow these steps:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-powered-waste-classification
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Application Locally

```bash
streamlit run app.py
```

The application will start at:

```text
http://localhost:8501
```

---

## Using the Application

1. **Register**: Create a new account with your credentials
2. **Login**: Access your account dashboard
3. **Upload/Capture**: Choose to upload an image or capture one using your device camera
4. **Configure**: Adjust the confidence threshold if needed (default: 0.5)
5. **Analyze**: Click **Analyze** to run waste detection
6. **Review Results**: See annotated image with bounding boxes and confidence scores
7. **History**: Access all your previous scans in the history section

---

## 🚀 Deployment

This application is deployed on **Streamlit Community Cloud**, a free cloud platform for hosting Streamlit apps.

### Deployment Details

- **Platform**: Streamlit Community Cloud
- **URL**: https://ai-wasteclassification.streamlit.app/
- **Status**: ✅ Live and accessible
- **Environment**: Python 3.9+, PyTorch with CPU inference
- **Database**: SQLite (persisted)
- **Model**: YOLO11 (waste_model.pt)

### To Deploy Your Own Instance

1. Push your code to a GitHub repository
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Create a new app and connect your GitHub repo
4. Select the branch and `app.py` as the entry point
5. Deploy!

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

- 🎥 Real-time video stream detection
- ♻️ Recycling recommendations based on detected waste
- 📊 Analytics dashboard showing detection patterns
- 🌍 Multi-language support
- 📱 Mobile app (React Native)
- 🤝 Community contribution system for model improvements
- 🔄 Model versioning and A/B testing
- 🎯 Fine-tuning on regional waste patterns
- ☁️ Batch processing for bulk image analysis
- 📈 Advanced metrics and reporting

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 💬 Support & Feedback

For issues, bug reports, or feature requests, please open an issue on GitHub. We welcome contributions and feedback from the community!

---

## 🙏 Acknowledgments

* [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) - Object detection framework
* [Streamlit](https://streamlit.io/) - Web app framework
* [Roboflow](https://roboflow.com/) - Dataset management platform
* PyTorch and the open-source ML community


import os

from roboflow import Roboflow

api_key = os.getenv("ROBOFLOW_API_KEY")
if not api_key:
    raise RuntimeError("Set ROBOFLOW_API_KEY in your environment before running this script.")

rf = Roboflow(api_key=api_key)
project = rf.workspace("sujals-workspace-5hfno").project("waste-dataset-v5-prev-wpqez")
version = project.version(2)
dataset = version.download("yolov11")

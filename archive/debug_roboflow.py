import os

from roboflow import Roboflow

api_key = os.getenv("ROBOFLOW_API_KEY")
if not api_key:
    raise RuntimeError("Set ROBOFLOW_API_KEY in your environment before running this script.")

rf = Roboflow(api_key=api_key)
print("Roboflow connection successful.")

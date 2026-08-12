import time
import numpy as np
from PIL import Image
from core.inference import load_model, run_inference
import warnings
warnings.filterwarnings("ignore")

def benchmark_latency(num_warmup=5, num_runs=50):
    print("Loading model...")
    model = load_model()
    if not model:
        print("Model not found!")
        return

    print("Generating dummy test image (640x640)...")
    # Create a random RGB image to simulate a camera frame
    dummy_img_array = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    dummy_img = Image.fromarray(dummy_img_array)

    print(f"Running {num_warmup} warmup iterations...")
    for _ in range(num_warmup):
        run_inference(dummy_img)

    print(f"Running {num_runs} benchmark iterations...")
    latencies = []
    for _ in range(num_runs):
        start = time.perf_counter()
        run_inference(dummy_img)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)

    mean_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)
    min_latency = np.min(latencies)
    max_latency = np.max(latencies)

    print("\n--- Latency Benchmark Results (CPU) ---")
    print(f"Mean Inference Time: {mean_latency:.2f} ms")
    print(f"95th Percentile:     {p95_latency:.2f} ms")
    print(f"Min Inference Time:  {min_latency:.2f} ms")
    print(f"Max Inference Time:  {max_latency:.2f} ms")
    print("---------------------------------------")

if __name__ == "__main__":
    benchmark_latency()

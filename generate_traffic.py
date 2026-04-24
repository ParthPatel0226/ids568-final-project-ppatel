import sys
import time
import random
sys.path.insert(0, 'src/monitoring')

import requests

samples = [
    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
    {"sepal_length": 4.9, "sepal_width": 3.0, "petal_length": 1.4, "petal_width": 0.2},
    {"sepal_length": 6.4, "sepal_width": 3.2, "petal_length": 4.5, "petal_width": 1.5},
    {"sepal_length": 5.7, "sepal_width": 2.8, "petal_length": 4.1, "petal_width": 1.3},
    {"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 6.0, "petal_width": 2.5},
    {"sepal_length": 7.2, "sepal_width": 3.6, "petal_length": 6.1, "petal_width": 2.5},
    {"sepal_length": 6.0, "sepal_width": 2.7, "petal_length": 5.1, "petal_width": 1.6},
    {"sepal_length": 5.8, "sepal_width": 2.7, "petal_length": 5.1, "petal_width": 1.9},
]

print("Generating 200 synthetic requests...")
success = 0
errors = 0

for i in range(200):
    sample = random.choice(samples)
    noisy = {k: round(v + random.gauss(0, 0.1), 2) for k, v in sample.items()}
    noisy["sepal_length"] = max(4.0, min(8.5, noisy["sepal_length"]))
    noisy["sepal_width"]  = max(1.5, min(5.0, noisy["sepal_width"]))
    noisy["petal_length"] = max(0.5, min(8.0, noisy["petal_length"]))
    noisy["petal_width"]  = max(0.0, min(3.5, noisy["petal_width"]))

    try:
        r = requests.post("http://localhost:8000/predict", json=noisy, timeout=2)
        if r.status_code == 200:
            success += 1
        else:
            errors += 1
    except Exception as e:
        errors += 1

    time.sleep(0.05)

    if (i + 1) % 50 == 0:
        print(f"  Sent {i+1}/200 requests ({success} ok, {errors} errors)")

print(f"Done! {success} success, {errors} errors")

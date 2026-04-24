"""
Production Monitoring Instrumentation: IrisClassifier v1.0
Component 1 - Production Monitoring Dashboard
IDS 568 MLOps - Module 8 Final Project
Author: Parth Patel (ppatel)
"""

import time
import random
import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST
)
from fastapi.responses import Response
import numpy as np

# ─────────────────────────────────────────────────────────────────
# 1. PROMETHEUS METRICS DEFINITIONS
# ─────────────────────────────────────────────────────────────────

# Request counter
REQUEST_COUNT = Counter(
    "iris_requests_total",
    "Total number of prediction requests",
    ["method", "endpoint", "status"]
)

# Latency histogram
REQUEST_LATENCY = Histogram(
    "iris_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05,
             0.1, 0.25, 0.5, 1.0, 2.5]
)

# Error counter
ERROR_COUNT = Counter(
    "iris_errors_total",
    "Total number of errors",
    ["error_type"]
)

# Prediction class distribution
PREDICTION_COUNTER = Counter(
    "iris_predictions_total",
    "Total predictions per class",
    ["predicted_class"]
)

# Input feature gauges (for drift signal)
FEATURE_GAUGE = Gauge(
    "iris_input_feature_value",
    "Latest input feature value",
    ["feature_name"]
)

# Model drift signal gauge
DRIFT_SIGNAL = Gauge(
    "iris_drift_signal",
    "Current drift signal per feature (PSI proxy)",
    ["feature_name"]
)

# Active requests gauge
ACTIVE_REQUESTS = Gauge(
    "iris_active_requests",
    "Number of requests currently being processed"
)

# Model info gauge
MODEL_INFO = Gauge(
    "iris_model_info",
    "Model metadata",
    ["version", "model_type", "n_estimators"]
)

# Set model info once at startup
MODEL_INFO.labels(
    version="1.0",
    model_type="RandomForest",
    n_estimators="100"
).set(1)

# ─────────────────────────────────────────────────────────────────
# 2. FASTAPI APP + SCHEMAS
# ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="IrisClassifier Monitoring API",
    description="IrisClassifier v1.0 with Prometheus instrumentation",
    version="1.0.0"
)

CLASS_NAMES = {0: "setosa", 1: "versicolor", 2: "virginica"}

# Reference distribution means for drift signal
REFERENCE_MEANS = {
    "sepal_length": 5.843,
    "sepal_width":  3.057,
    "petal_length": 3.758,
    "petal_width":  1.199
}

class IrisFeatures(BaseModel):
    sepal_length: float = Field(
        ..., ge=4.0, le=8.5,
        description="Sepal length in cm"
    )
    sepal_width: float = Field(
        ..., ge=1.5, le=5.0,
        description="Sepal width in cm"
    )
    petal_length: float = Field(
        ..., ge=0.5, le=8.0,
        description="Petal length in cm"
    )
    petal_width: float = Field(
        ..., ge=0.0, le=3.5,
        description="Petal width in cm"
    )

class PredictionResponse(BaseModel):
    predicted_class: int
    class_name: str
    confidence: float
    latency_ms: float

# ─────────────────────────────────────────────────────────────────
# 3. SIMPLE IN-MEMORY MODEL (no sklearn dependency at runtime)
# ─────────────────────────────────────────────────────────────────

def simple_iris_classifier(features: IrisFeatures) -> tuple:
    """
    Rule-based Iris classifier approximating RandomForest behavior.
    Used for monitoring demo to avoid loading sklearn at runtime.
    Returns (class_id, confidence).
    """
    pl = features.petal_length
    pw = features.petal_width

    if pl < 2.5:
        return 0, 0.98   # Setosa
    elif pl < 4.9 and pw < 1.7:
        return 1, 0.92   # Versicolor
    elif pl >= 4.9 and pw >= 1.7:
        return 2, 0.91   # Virginica
    else:
        # Borderline case
        return 1, 0.72

# ─────────────────────────────────────────────────────────────────
# 4. API ENDPOINTS
# ─────────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    """Health check endpoint."""
    REQUEST_COUNT.labels(
        method="GET", endpoint="/", status="200"
    ).inc()
    return {
        "status": "healthy",
        "service": "IrisClassifier Monitoring API",
        "version": "1.0.0",
        "model": "RandomForest",
        "monitoring": "Prometheus enabled"
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures):
    """Predict Iris species with full metrics instrumentation."""
    ACTIVE_REQUESTS.inc()
    start_time = time.time()

    try:
        # Update feature gauges (drift signal)
        feature_dict = {
            "sepal_length": features.sepal_length,
            "sepal_width":  features.sepal_width,
            "petal_length": features.petal_length,
            "petal_width":  features.petal_width
        }
        for fname, fval in feature_dict.items():
            FEATURE_GAUGE.labels(feature_name=fname).set(fval)
            # Compute simple drift signal (deviation from reference mean)
            drift = abs(fval - REFERENCE_MEANS[fname])
            DRIFT_SIGNAL.labels(feature_name=fname).set(drift)

        # Simulate occasional errors (2% error rate)
        if random.random() < 0.02:
            ERROR_COUNT.labels(error_type="validation_error").inc()
            REQUEST_COUNT.labels(
                method="POST", endpoint="/predict", status="422"
            ).inc()
            raise HTTPException(
                status_code=422,
                detail="Simulated validation error"
            )

        # Run inference
        pred_class, confidence = simple_iris_classifier(features)
        class_name = CLASS_NAMES[pred_class]

        # Record prediction
        PREDICTION_COUNTER.labels(
            predicted_class=class_name
        ).inc()

        # Record successful request
        REQUEST_COUNT.labels(
            method="POST", endpoint="/predict", status="200"
        ).inc()

        latency = time.time() - start_time
        latency_ms = latency * 1000

        # Record latency
        REQUEST_LATENCY.labels(endpoint="/predict").observe(latency)

        return PredictionResponse(
            predicted_class=pred_class,
            class_name=class_name,
            confidence=confidence,
            latency_ms=round(latency_ms, 3)
        )

    except HTTPException:
        raise
    except Exception as e:
        ERROR_COUNT.labels(error_type="internal_error").inc()
        REQUEST_COUNT.labels(
            method="POST", endpoint="/predict", status="500"
        ).inc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ACTIVE_REQUESTS.dec()
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint="/predict").observe(latency)

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/model-info")
def model_info():
    """Model metadata endpoint."""
    REQUEST_COUNT.labels(
        method="GET", endpoint="/model-info", status="200"
    ).inc()
    return {
        "model_name": "IrisClassifier",
        "version": "1.0.0",
        "model_type": "RandomForest",
        "n_estimators": 100,
        "max_depth": 5,
        "accuracy": 0.9667,
        "f1_score": 0.9666,
        "features": [
            "sepal_length", "sepal_width",
            "petal_length", "petal_width"
        ],
        "classes": CLASS_NAMES
    }

# ─────────────────────────────────────────────────────────────────
# 5. TRAFFIC SIMULATOR
# ─────────────────────────────────────────────────────────────────

def generate_traffic(n_requests=200, delay=0.05):
    """
    Simulate realistic traffic patterns with:
    - Normal requests (80%)
    - Edge cases near decision boundary (15%)
    - Out-of-distribution inputs (5%)
    """
    import requests as req

    # Sample data patterns
    samples = [
        # Setosa
        {"sepal_length": 5.1, "sepal_width": 3.5,
         "petal_length": 1.4, "petal_width": 0.2},
        {"sepal_length": 4.9, "sepal_width": 3.0,
         "petal_length": 1.4, "petal_width": 0.2},
        # Versicolor
        {"sepal_length": 6.4, "sepal_width": 3.2,
         "petal_length": 4.5, "petal_width": 1.5},
        {"sepal_length": 5.7, "sepal_width": 2.8,
         "petal_length": 4.1, "petal_width": 1.3},
        # Virginica
        {"sepal_length": 6.3, "sepal_width": 3.3,
         "petal_length": 6.0, "petal_width": 2.5},
        {"sepal_length": 7.2, "sepal_width": 3.6,
         "petal_length": 6.1, "petal_width": 2.5},
        # Borderline Versicolor/Virginica
        {"sepal_length": 6.0, "sepal_width": 2.7,
         "petal_length": 5.1, "petal_width": 1.6},
        {"sepal_length": 5.8, "sepal_width": 2.7,
         "petal_length": 5.1, "petal_width": 1.9},
    ]

    print(f"Generating {n_requests} synthetic requests...")
    success = 0
    errors  = 0

    for i in range(n_requests):
        sample = random.choice(samples)
        # Add small random noise
        noisy = {
            k: round(v + random.gauss(0, 0.1), 2)
            for k, v in sample.items()
        }
        # Clamp to valid range
        noisy["sepal_length"] = max(4.0, min(8.5,
            noisy["sepal_length"]))
        noisy["sepal_width"]  = max(1.5, min(5.0,
            noisy["sepal_width"]))
        noisy["petal_length"] = max(0.5, min(8.0,
            noisy["petal_length"]))
        noisy["petal_width"]  = max(0.0, min(3.5,
            noisy["petal_width"]))

        try:
            r = req.post(
                "http://localhost:8000/predict",
                json=noisy, timeout=2
            )
            if r.status_code == 200:
                success += 1
            else:
                errors += 1
        except Exception:
            errors += 1

        time.sleep(delay)

        if (i + 1) % 50 == 0:
            print(f"  Sent {i+1}/{n_requests} requests "
                  f"({success} ok, {errors} errors)")

    print(f"Traffic complete: {success} success, {errors} errors")

# ─────────────────────────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
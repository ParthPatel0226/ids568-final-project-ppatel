\# Model Card: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project

\*\*Last Updated:\*\* April 2026



\---



\## 1. Model Overview



| Field | Details |

|-------|---------|

| Model Name | IrisClassifier |

| Model Type | Random Forest Classifier |

| Version | 1.0 (Production) |

| Framework | scikit-learn 1.4.0 |

| Task | Multi-class classification (3 classes) |

| Serving Method | FastAPI REST API (Cloud Run + Cloud Function) |

| Hardware | CPU-only inference, no GPU required |



\---



\## 2. Intended Use



\### Primary Use Case

Classify Iris flower species (Setosa, Versicolor, Virginica) based on

4 sepal/petal measurements. Designed as a demonstration system for

MLOps monitoring, governance, and operational best practices.



\### Intended Users

\- MLOps engineers learning production deployment patterns

\- Students and instructors in IDS 568 MLOps course

\- Developers evaluating scikit-learn serving patterns



\### Out-of-Scope Applications

\- Any real-world botanical or scientific classification

\- Medical, legal, or financial decision-making

\- Production systems handling sensitive or personal data

\- Any classification task beyond the 3 Iris species



\---



\## 3. Training Data



| Field | Details |

|-------|---------|

| Dataset | UCI Iris Dataset (via sklearn.datasets.load\_iris) |

| Size | 150 samples, 4 features, 3 classes |

| Classes | Setosa (0), Versicolor (1), Virginica (2) |

| Split | 80% train (120 samples), 20% test (30 samples) |

| Random State | 42 (fixed for reproducibility) |

| Preprocessing | Column name normalization, dropna() |

| Data Hash | Logged per run in MLflow for lineage tracking |



\### Features

| Feature | Description | Unit |

|---------|-------------|------|

| sepal\_length | Length of sepal | cm |

| sepal\_width | Width of sepal | cm |

| petal\_length | Length of petal | cm |

| petal\_width | Width of petal | cm |



\---



\## 4. Performance Metrics



Evaluated on held-out 20% test set (30 samples, random\_state=42):



| Metric | Value | Threshold |

|--------|-------|-----------|

| Accuracy | 0.9667 | >= 0.85 |

| F1 Score (weighted) | 0.9666 | >= 0.85 |

| Inference Latency (p50) | \~2ms | < 100ms |

| Inference Latency (p99) | \~8ms | < 200ms |



\### Per-Class Performance

| Class | Precision | Recall | F1 |

|-------|-----------|--------|----|

| Setosa (0) | 1.00 | 1.00 | 1.00 |

| Versicolor (1) | 0.92 | 0.92 | 0.92 |

| Virginica (2) | 0.92 | 0.92 | 0.92 |



> Note: Versicolor and Virginica are harder to separate due to

> overlapping feature distributions - the primary failure mode.



\---



\## 5. Limitations \& Failure Modes



| Limitation | Description | Severity |

|------------|-------------|----------|

| Versicolor/Virginica confusion | Overlapping petal measurements cause \~8% misclassification between these two classes | Medium |

| Distribution shift sensitivity | Model trained on balanced 50/50/50 data; skewed real-world distributions will degrade accuracy | High |

| Feature range assumptions | Inputs outside training range \[4.3-7.9cm sepal, 1.0-6.9cm petal] are extrapolations with no reliability guarantee | High |

| No uncertainty output | Model returns hard class labels only; no confidence scores surfaced in API v1.0 | Medium |

| Static model | No online learning; model does not adapt to new data without retraining | Low |



\---



\## 6. Ethical Risks \& Considerations



| Risk | Assessment |

|------|------------|

| Bias | Dataset is balanced (50 samples per class); minimal class bias. No demographic data involved. |

| Privacy | No PII collected or processed. Input features are botanical measurements only. |

| Fairness | Not applicable - no protected characteristics in this domain |

| Misuse potential | Low - botanical classification has no known misuse pathways |

| Environmental | Minimal - CPU-only inference, low energy footprint |



\---



\## 7. Monitoring \& Drift Signals



The following signals are tracked in production (see Component 1 dashboard):



\- \*\*Prediction latency\*\* (p50, p99) - alert if p99 > 200ms

\- \*\*Error rate\*\* - alert if > 1% over 5-minute window

\- \*\*Input feature distributions\*\* - alert if PSI > 0.2 vs reference

\- \*\*Class distribution\*\* - alert if any class drops below 10% of predictions

\- \*\*Model accuracy proxy\*\* - tracked via A/B experiment results (see Component 2)



\---



\## 8. Model Lineage



Raw Data (sklearn Iris)

|

v

preprocess.py (normalize columns, dropna, hash)

|

v

train.py (RandomForest, n=100, depth=5, seed=42)

|

v

MLflow Run (logged: params, metrics, artifacts, hashes)

|

v

model\_validation.py (quality gate: acc>=0.85, f1>=0.85)

|

v

MLflow Registry (None -> Staging -> Production)

|

v

FastAPI Service (Cloud Run + Cloud Function)

|

v

Prometheus Metrics + Grafana Dashboard



See `docs/lineage-diagram.png` for visual representation.



\---



\## 9. Version History



| Version | Date | Change | Approved By |

|---------|------|--------|-------------|

| 1.0 | 2026-04-24 | Initial production release | ppatel |



\---



\## 10. Contact \& Governance



\*\*Model Owner:\*\* Parth Patel (ppatel@uic.edu)

\*\*Governance Framework:\*\* NIST AI RMF

\*\*Review Cycle:\*\* Monthly or upon accuracy drop below 0.85

\*\*Retraining Trigger:\*\* Feature drift PSI > 0.2 OR accuracy < 0.85


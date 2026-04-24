# IDS 568 MLOps — Final Project
### Production Monitoring, Governance & Evaluation Framework

**Author:** Parth Patel | **NetID:** ppatel | **Course:** IDS 568 MLOps — Module 8  
**University:** University of Illinois Chicago | **Date:** April 2026

---

## Overview

This capstone project implements a **complete production operations framework** for `IrisClassifier v1.0` — a RandomForest-based Iris species classifier built across all prior course milestones. The system demonstrates end-to-end MLOps practices including live monitoring, statistical experimentation, governance documentation, drift detection, and AI risk assessment.

> **Base System:** RandomForest classifier (n=100, depth=5) trained on UCI Iris dataset, served via FastAPI on GCP Cloud Run — built on Milestone 1 (model serving) and Milestone 3 (MLflow experiment tracking).

---

## Project Components

| # | Component | Description | Key Files |
|---|-----------|-------------|-----------|
| C1 | **Production Monitoring Dashboard** | Prometheus + Grafana instrumentation with 10 live panels | `src/monitoring/instrumentation.py` |
| C2 | **A/B Test Design & Simulation** | 1000-trial bootstrap experiment comparing model variants | `src/ab_test/simulation.py` |
| C3 | **Model Card & Governance Packet** | Full lineage, risk register, audit trail | `docs/model-card.md` |
| C4 | **Data Integrity & Drift Detection** | PSI + KS tests across 4 features with visualizations | `src/drift/drift_detection.py` |
| C5 | **AI Risk Assessment** | NIST AI RMF-aligned governance review, 14 risks scored | `docs/governance-review.md` |

---

## Repository Structure

```
ids568-final-project-ppatel/
├── src/
│   ├── monitoring/
│   │   └── instrumentation.py        # C1: FastAPI + Prometheus metrics (7 metric types)
│   ├── ab_test/
│   │   └── simulation.py             # C2: 1000-trial bootstrap A/B simulation
│   └── drift/
│       └── drift_detection.py        # C4: PSI + KS + outlier detection
│
├── docs/
│   ├── dashboard-interpretation.md   # C1: 10-panel dashboard analysis
│   ├── experiment-specification.md   # C2: Hypothesis, power analysis, decision rules
│   ├── recommendation-memo.md        # C2: Ship A / Ship B decision memo
│   ├── model-card.md                 # C3: Performance, limitations, ethical risks
│   ├── risk-register.md              # C3: 13 risks across 4 categories
│   ├── lineage-diagram.md            # C3: Data → training → deployment flow
│   ├── lineage-diagram.png           # C3: Visual lineage diagram
│   ├── audit-trail.md                # C3: Human-readable event log
│   ├── drift-diagnostic-report.md    # C4: PSI scores + business impact analysis
│   ├── governance-review.md          # C5: NIST AI RMF structured review
│   ├── risk-matrix.md                # C5: Likelihood × severity matrix (14 risks)
│   ├── system-boundary-diagram.png   # C5: Full pipeline boundary diagram
│   └── cto-memo.md                   # C5: Executive summary for leadership
│
├── dashboards/
│   └── grafana-export.json           # C1: Grafana dashboard config (importable)
│
├── logs/
│   └── audit-trail.json              # C3: Machine-readable audit trail (EVT-001 to EVT-007)
│
├── visualizations/
│   ├── drift_distributions.png       # C4: Reference vs production feature histograms
│   ├── psi_summary.png               # C4: PSI bar chart with threshold lines
│   ├── drift_over_time.png           # C4: PSI across 8 time windows
│   ├── label_distribution.png        # C4: Class label comparison
│   ├── ab_test_distributions.png     # C2: Model A vs B metric distributions
│   ├── ab_test_ci.png                # C2: 95% confidence intervals
│   ├── dashboard-screenshot-1.png    # C1: Live Grafana dashboard (top panels)
│   ├── dashboard-screenshot-2.png    # C1: Live Grafana dashboard (middle panels)
│   └── dashboard-screenshot-3.png    # C1: Live Grafana dashboard (bottom panels)
│
├── generate_traffic.py               # Synthetic traffic generator (200 requests)
├── create_diagrams.py                # Generates lineage + system boundary PNGs
├── prometheus.yml                    # Prometheus scrape config (5s interval)
├── docker-compose.yml                # Monitoring stack (Prometheus + Grafana)
├── requirements.txt                  # Pinned Python dependencies
└── README.md                         # This file
```

---

## Quick Start — Reproduce All Results

### Prerequisites
- Python 3.10+
- Docker Desktop
- Git

### 1. Clone & Install
```bash
git clone https://github.com/ParthPatel0226/ids568-final-project-ppatel.git
cd ids568-final-project-ppatel
pip install -r requirements.txt
```

### 2. Run Drift Detection (Component 4)
```bash
python src/drift/drift_detection.py
# Outputs 4 PNGs to visualizations/
# Takes ~10 seconds
```

### 3. Run A/B Test Simulation (Component 2)
```bash
python src/ab_test/simulation.py
# Outputs 2 PNGs to visualizations/
# Takes ~2 minutes (1000 bootstrap trials)
```

### 4. Run Monitoring Dashboard (Component 1)

**Terminal 1 — Start the instrumented API:**
```bash
python src/monitoring/instrumentation.py
# FastAPI running at http://localhost:8000
```

**Terminal 2 — Start Prometheus + Grafana:**
```bash
docker-compose up -d
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000  (admin/admin)
```

**Terminal 3 — Generate synthetic traffic:**
```bash
python generate_traffic.py
# Sends 200 requests with realistic patterns
```

**Import the dashboard:**
```bash
curl -X POST http://admin:admin@localhost:3000/api/dashboards/import \
  -H "Content-Type: application/json" \
  -d @dashboards/grafana-export.json
```

**View live dashboard:**
```
http://localhost:3000/d/6a4ec3a7-e351-47d4-82f2-7cae950b1017/irisclassifier-v1-0-production-monitoring
```

---

## Component Results

### C1: Production Monitoring Dashboard

Instrumented FastAPI service with **7 Prometheus metric types** — counters, histograms, and gauges — covering all required signal categories.

| Metric | Observed Value | Threshold | Status |
|--------|---------------|-----------|--------|
| Request Rate | 0.172 req/sec | > 0 | OK |
| P99 Latency | ~1ms | < 200ms | OK |
| Error Rate | ~2% (simulated) | < 1% | WARNING |
| petal_length drift | 2.5 (deviation) | < 2.0 | WARNING |
| Active Requests | 0 (between bursts) | < 10 | OK |

**Stack:** Prometheus (pull-based, 5s scrape) + Grafana (10 panels, 5s refresh)  
See: [`docs/dashboard-interpretation.md`](docs/dashboard-interpretation.md)

---

### C2: A/B Test Design & Simulation

Compared **Model A** (n=100, depth=5, production) vs **Model B** (n=200, depth=7, candidate) across 1000 bootstrap trials.

| Metric | Model A | Model B | Difference | Significant? |
|--------|---------|---------|------------|-------------|
| Accuracy | 0.9537 | 0.9529 | -0.0008 | NO (p=1.0) |
| F1 Score | 0.9537 | 0.9529 | -0.0008 | NO (p=1.0) |
| Latency | 74ms | 146ms | +72ms (1.97x) | YES — GUARDRAIL FAIL |

**Decision: KEEP MODEL A** — Model B failed the latency guardrail (1.97x > 1.5x threshold) with zero accuracy benefit.

See: [`docs/recommendation-memo.md`](docs/recommendation-memo.md)

---

### C3: Model Card & Governance Packet

| Artifact | Description |
|----------|-------------|
| Model Card | Performance (96.7%), training data, limitations, ethical risks, intended use |
| Lineage Diagram | Full pipeline: data → preprocess → train → MLflow → registry → deploy → monitor |
| Risk Register | 13 risks across bias, robustness, privacy, compliance categories |
| Audit Trail | 7 lifecycle events (EVT-001 to EVT-007) with timestamps and approvals |

See: [`docs/model-card.md`](docs/model-card.md) | [`logs/audit-trail.json`](logs/audit-trail.json)

---

### C4: Data Integrity & Drift Detection

PSI and KS tests comparing reference (UCI Iris training) vs simulated production distribution.

| Feature | PSI Score | KS p-value | Status |
|---------|-----------|-----------|--------|
| petal_width | **2.1935** | 0.0009 | CRITICAL |
| petal_length | **1.7533** | 0.0000 | CRITICAL |
| sepal_length | 0.4360 | 0.1804 | CRITICAL |
| sepal_width | 0.0856 | 0.2308 | OK |

**Recommendation:** Immediate retraining required. Petal features have shifted beyond decision boundaries.

See: [`docs/drift-diagnostic-report.md`](docs/drift-diagnostic-report.md)

---

### C5: AI Risk Assessment

NIST AI RMF-aligned governance review covering data security, compliance, hallucination analogues, and tool-misuse pathways.

| Level | Count | Top Risk |
|-------|-------|---------|
| Critical | 1 | R01: Feature drift (ACTIVE) |
| High | 1 | R02: Latency guardrail (MITIGATED by C2) |
| Medium | 10 | R03-R12 (5 open, 5 mitigated) |
| Low | 2 | R13-R14 (mitigated) |

See: [`docs/cto-memo.md`](docs/cto-memo.md) | [`docs/risk-matrix.md`](docs/risk-matrix.md)

---

## Component Cross-References

The components tell one coherent story — each informs the others:

| Component | References |
|-----------|-----------|
| C1 Monitoring alerts | Uses drift thresholds from C4 (PSI > 0.2) |
| C2 A/B latency finding | Validates why p99 monitoring (C1) matters |
| C3 Model card limits | Maps directly to risks identified in C5 |
| C4 Drift trigger | Documented as EVT-006 in C3 audit trail |
| C5 Risk mitigations | Reference monitoring capabilities from C1 |

---

## Lessons Learned

1. **Monitoring requires interpretation** — raw metrics without diagnostic reasoning lose points and miss the point. The interpretation document was as important as the instrumentation code.

2. **A/B tests need guardrail metrics** — Model B's latency was 1.97x higher with zero accuracy benefit. Without the guardrail, this candidate would have degraded production based on naive hyperparameter assumptions.

3. **Drift detection connects everything** — the PSI findings in C4 appeared in the C1 dashboard drift signals, drove EVT-006 in the C3 audit trail, and produced the only Critical risk in C5. All components are part of one system story.

4. **Governance is operational, not just documentation** — the model card, audit trail, and risk register change with every deployment decision. They are accountability tools, not checkbox exercises.

5. **Start monitoring before you need it** — having a dashboard baseline before drift occurs means you have reference data for comparison when anomalies appear.

---

## Prior Milestone Repositories

| Milestone | Repository | Focus |
|-----------|-----------|-------|
| M0 | [Parth_Ids568-ML-Ops](https://github.com/ParthPatel0226/Parth_Ids568-ML-Ops) | Reproducible environments, CI/CD |
| M1 | [mlops-milestone1-model-serving](https://github.com/ParthPatel0226/mlops-milestone1-model-serving) | FastAPI + Cloud Run + Cloud Function |
| M3 | [ids568-milestone3-ppatel](https://github.com/ParthPatel0226/ids568-milestone3-ppatel) | Airflow + MLflow + quality gate |
| M4 | [ids568-milestone4-ppatel](https://github.com/ParthPatel0226/ids568-milestone4-ppatel) | PySpark distributed processing |

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green?logo=fastapi)
![Prometheus](https://img.shields.io/badge/Prometheus-latest-orange?logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-latest-orange?logo=grafana)
![Docker](https://img.shields.io/badge/Docker-29.4.0-blue?logo=docker)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.0-orange?logo=scikit-learn)
![MLflow](https://img.shields.io/badge/MLflow-2.10.2-blue?logo=mlflow)
![GCP](https://img.shields.io/badge/GCP-Cloud_Run-blue?logo=googlecloud)

---

*IDS 568 MLOps — Module 8 Final Project | University of Illinois Chicago | April 2026*
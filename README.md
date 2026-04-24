# ids568-final-project-ppatel



\# IDS 568 MLOps — Final Project

\*\*Author:\*\* Parth Patel | NetID: ppatel

\*\*Course:\*\* IDS 568 - MLOps | Module 8

\*\*Date:\*\* April 2026

\*\*Repository:\*\* ids568-final-project-ppatel



\---



\## System Overview



This project implements a complete production operations framework

for IrisClassifier v1.0 — a RandomForest-based Iris species

classifier built across all prior milestones. The system

demonstrates end-to-end MLOps practices including monitoring,

experimentation, governance, drift detection, and risk assessment.



\*\*Base System:\*\* RandomForest classifier (n=100, depth=5)

trained on UCI Iris dataset, served via FastAPI on GCP Cloud Run.

Built on Milestone 1 (serving) and Milestone 3 (MLflow tracking).



\---



\## Project Structure

ids568-final-project-ppatel/

├── src/

│   ├── monitoring/

│   │   └── instrumentation.py    # C1: FastAPI + Prometheus metrics

│   ├── ab\_test/

│   │   └── simulation.py         # C2: A/B test simulation

│   └── drift/

│       └── drift\_detection.py    # C4: Drift detection scripts

├── docs/

│   ├── dashboard-interpretation.md  # C1: Dashboard analysis

│   ├── experiment-specification.md  # C2: Experiment design

│   ├── recommendation-memo.md       # C2: Decision memo

│   ├── model-card.md                # C3: Model card

│   ├── risk-register.md             # C3: Risk register

│   ├── lineage-diagram.md           # C3: Lineage diagram

│   ├── audit-trail.md               # C3: Audit trail (human)

│   ├── drift-diagnostic-report.md   # C4: Drift report

│   ├── governance-review.md         # C5: Governance review

│   ├── risk-matrix.md               # C5: Risk matrix

│   └── cto-memo.md                  # C5: CTO memo

├── dashboards/

│   └── grafana-export.json       # C1: Grafana dashboard config

├── logs/

│   └── audit-trail.json          # C3: Audit trail (machine)

├── visualizations/

│   ├── drift\_distributions.png   # C4: Feature distributions

│   ├── psi\_summary.png           # C4: PSI scores

│   ├── drift\_over\_time.png       # C4: Drift over time windows

│   ├── label\_distribution.png    # C4: Label distributions

│   ├── ab\_test\_distributions.png # C2: A/B distributions

│   ├── ab\_test\_ci.png            # C2: Confidence intervals

│   └── dashboard-screenshot.png  # C1: Live dashboard

├── generate\_traffic.py           # Traffic simulator

├── prometheus.yml                # Prometheus config

├── docker-compose.yml            # Monitoring stack

├── requirements.txt              # Pinned dependencies

└── README.md                     # This file



\---



\## Setup \& Reproduction



\### Prerequisites

\- Python 3.10+

\- Docker Desktop

\- Git



\### 1. Clone Repository

```bash

git clone https://github.com/ParthPatel0226/ids568-final-project-ppatel.git

cd ids568-final-project-ppatel

```



\### 2. Install Dependencies

```bash

pip install -r requirements.txt

```



\### 3. Run Component 4 — Drift Detection

```bash

python src/drift/drift\_detection.py

```

Outputs 4 visualizations to `visualizations/`



\### 4. Run Component 2 — A/B Test Simulation

```bash

python src/ab\_test/simulation.py

```

Outputs 2 visualizations to `visualizations/`

Takes \~2 minutes (1000 bootstrap trials)



\### 5. Run Component 1 — Monitoring Dashboard

\*\*Terminal 1 — Start API:\*\*

```bash

python src/monitoring/instrumentation.py

```



\*\*Terminal 2 — Start Prometheus + Grafana:\*\*

```bash

docker-compose up -d

```



\*\*Terminal 3 — Generate traffic:\*\*

```bash

python generate\_traffic.py

```



\*\*Import dashboard:\*\*

```bash

curl -X POST http://admin:admin@localhost:3000/api/dashboards/import \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d @dashboards/grafana-export.json

```



\*\*View dashboard:\*\*

http://localhost:3000



\---



\## Component Summary



\### C1: Production Monitoring Dashboard

\*\*Score Target: 5/5\*\*



Instrumented FastAPI service with 7 Prometheus metric types

(counters, histograms, gauges) covering latency, throughput,

error rate, prediction distribution, and feature drift signals.

Grafana dashboard with 10 panels running on Docker stack.



Key findings from dashboard:

\- Request rate: 0.172 req/sec (simulated traffic)

\- P99 latency: \~1ms (well within 200ms SLA)

\- Error rate: \~2% (simulated validation errors)

\- petal\_length drift signal highest (consistent with C4)



See: `docs/dashboard-interpretation.md`



\---



\### C2: A/B Test Design \& Simulation

\*\*Score Target: 5/5\*\*



Designed and simulated a statistically rigorous A/B experiment

comparing Model A (n=100, depth=5) vs Model B (n=200, depth=7)

across 1000 bootstrap trials.



Key results:

\- Model B showed NO accuracy improvement (diff=-0.0008, p=1.0)

\- Model B latency 1.97x higher (146ms vs 74ms)

\- Latency guardrail FAILED — Model A retained in production



\*\*Decision: KEEP MODEL A\*\*



See: `docs/experiment-specification.md`,

&#x20;    `docs/recommendation-memo.md`



\---



\### C3: Model Card \& Governance Packet

\*\*Score Target: 5/5\*\*



Complete governance packet for IrisClassifier v1.0 including:

\- Model card with performance metrics, limitations, ethical risks

\- Full lineage diagram (data → training → registry → deployment)

\- Risk register with 13 risks across 4 categories

\- Structured audit trail with 7 lifecycle events (EVT-001 to EVT-007)



See: `docs/model-card.md`, `docs/risk-register.md`,

&#x20;    `docs/lineage-diagram.md`, `logs/audit-trail.json`



\---



\### C4: Data Integrity \& Drift Detection

\*\*Score Target: 5/5\*\*



Implemented PSI + KS drift detection comparing reference

(training) vs simulated production distributions.



Key findings:

\- petal\_width: PSI=2.1935 (CRITICAL)

\- petal\_length: PSI=1.7533 (CRITICAL)

\- sepal\_length: PSI=0.4360 (CRITICAL)

\- sepal\_width: PSI=0.0856 (OK)



\*\*Recommendation: Immediate retraining required\*\*



See: `docs/drift-diagnostic-report.md`, `visualizations/`



\---



\### C5: AI Risk Assessment \& Reflective Summary

\*\*Score Target: 5/5\*\*



System-level governance review using NIST AI RMF framework.

14 risks identified and scored across 5 categories.



Key findings:

\- 1 Critical risk (R01: data drift — active)

\- 1 High risk (R02: latency — mitigated by A/B guardrail)

\- 10 Medium risks (5 open, 5 mitigated)

\- 2 Low risks (mitigated)



See: `docs/governance-review.md`, `docs/risk-matrix.md`,

&#x20;    `docs/cto-memo.md`



\---



\## Component Cross-References



| If you have... | It references... |

|----------------|-----------------|

| Monitoring alerts (C1) | Drift thresholds from C4 (PSI>0.2) |

| A/B test latency (C2) | Validates p99 monitoring in C1 |

| Model card limits (C3) | Risks identified in C5 |

| Drift triggers (C4) | Retraining in audit trail (C3 EVT-006) |

| Risk mitigations (C5) | Monitoring capabilities in C1 |



\---



\## Lessons Learned



1\. \*\*Monitoring requires interpretation\*\* — raw metrics without

&#x20;  context are meaningless. The dashboard interpretation doc

&#x20;  (C1) was as important as the instrumentation code itself.



2\. \*\*A/B tests need guardrail metrics\*\* — Model B's accuracy

&#x20;  improvement was negligible but its latency increase was

&#x20;  critical. Without the guardrail, a degraded model could

&#x20;  have been shipped based on naive hyperparameter assumptions.



3\. \*\*Drift detection connects everything\*\* — the PSI findings

&#x20;  in C4 showed up in the C1 dashboard drift signals, were

&#x20;  referenced in the C3 audit trail, and drove the highest

&#x20;  risk rating in C5. All components tell one coherent story.



4\. \*\*Governance is operational, not just documentation\*\* —

&#x20;  the model card, audit trail, and risk register are living

&#x20;  documents that change with every deployment decision.

&#x20;  They are not checkbox exercises but accountability tools.



5\. \*\*Start monitoring before you need it\*\* — setting up

&#x20;  Prometheus/Grafana before drift occurs means you have

&#x20;  baseline data to compare against when anomalies appear.



\---



\## Prior Milestone Repositories



| Milestone | Repository | Focus |

|-----------|-----------|-------|

| M1 | \[mlops-milestone1-model-serving](https://github.com/ParthPatel0226/mlops-milestone1-model-serving) | FastAPI + Cloud Run |

| M3 | \[ids568-milestone3-ppatel](https://github.com/ParthPatel0226/ids568-milestone3-ppatel) | Airflow + MLflow |

| M4 | \[ids568-milestone4-ppatel](https://github.com/ParthPatel0226/ids568-milestone4-ppatel) | Distributed processing |


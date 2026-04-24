\# Audit Trail: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel  

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project  

\*\*Last Updated:\*\* April 2026



\---



\## Purpose



This audit trail documents all significant events in the lifecycle of

the IrisClassifier system — including model version changes, approval

workflows, monitoring events, and interventions. It serves as the

official accountability record for governance and compliance review.



The machine-readable version of this trail is maintained in

`logs/audit-trail.json`. This document provides human-readable

summaries and commentary.



\---



\## Event Log



\### EVT-001 | Model Training | 2026-01-20

\- \*\*Type:\*\* Model Training \& Deployment

\- \*\*Version:\*\* v0.1-dev

\- \*\*Actor:\*\* ppatel

\- \*\*Action:\*\* Initial IrisClassifier trained using scikit-learn

&#x20; RandomForest on UCI Iris dataset. Deployed to GCP Cloud Run

&#x20; and Cloud Function as part of Milestone 1.

\- \*\*Outcome:\*\* Both endpoints live and tested. Accuracy 0.9667.

\- \*\*Approval:\*\* Self-approved (ppatel) — development milestone



\---



\### EVT-002 | Experiment Tracking | 2026-03-03

\- \*\*Type:\*\* MLflow Integration \& Registry Promotion

\- \*\*Version:\*\* v0.3-mlflow

\- \*\*Actor:\*\* ppatel

\- \*\*Action:\*\* Added MLflow experiment tracking (Milestone 3).

&#x20; Ran 5 experiments with varying hyperparameters:



| Run | Model | n\_estimators | max\_depth | Accuracy |

|-----|-------|-------------|-----------|----------|

| 1 | RandomForest | 50 | 3 | 0.9333 |

| 2 | RandomForest | 100 | 5 | 0.9667 |

| 3 | RandomForest | 200 | 10 | 0.9667 |

| 4 | RandomForest | 150 | 2 | 0.9000 |

| 5 | LogisticRegression | - | - | 0.9667 |



\- \*\*Decision:\*\* Run 2 (n=100, depth=5) selected as best —

&#x20; top accuracy with lowest complexity.

\- \*\*Registry:\*\* Promoted None -> Staging -> Production

\- \*\*Approval:\*\* Self-approved (ppatel) — passed quality gate

&#x20; (accuracy=0.9667 >= 0.85, f1=0.9666 >= 0.85)



\---



\### EVT-003 | Governance Review | 2026-04-24

\- \*\*Type:\*\* Documentation \& Governance

\- \*\*Version:\*\* v1.0

\- \*\*Actor:\*\* ppatel

\- \*\*Action:\*\* Full governance packet created for Module 8

&#x20; Final Project. System formally designated v1.0 Production.

&#x20; Created: model card, risk register, lineage diagram,

&#x20; audit trail.

\- \*\*Outcome:\*\* All governance documents committed to GitHub

\- \*\*Approval:\*\* Self-approved (ppatel)



\---



\### EVT-004 | Monitoring Deployment | 2026-04-24

\- \*\*Type:\*\* Observability Infrastructure

\- \*\*Version:\*\* v1.0

\- \*\*Actor:\*\* ppatel

\- \*\*Action:\*\* Prometheus metrics instrumentation added to

&#x20; FastAPI service. Grafana dashboard configured with:

&#x20; - Request latency (p50, p99)

&#x20; - Error rate

&#x20; - Request throughput

&#x20; - Input integrity anomaly signals

&#x20; - Drift indicators

\- \*\*Alert Thresholds Set:\*\*

&#x20; - Latency p99 > 200ms → WARNING

&#x20; - Error rate > 1% → CRITICAL

&#x20; - Drift PSI > 0.2 → WARNING

\- \*\*Outcome:\*\* Dashboard live with simulated traffic

\- \*\*Approval:\*\* Self-approved (ppatel)



\---



\### EVT-005 | A/B Test | 2026-04-24

\- \*\*Type:\*\* Experiment Design \& Simulation

\- \*\*Version:\*\* v1.0 (Model A) vs v1.1-candidate (Model B)

\- \*\*Actor:\*\* ppatel

\- \*\*Action:\*\* Designed and simulated A/B test comparing:

&#x20; - Model A: RandomForest n=100, depth=5 (current production)

&#x20; - Model B: RandomForest n=200, depth=7 (candidate)

\- \*\*Result:\*\* Statistical evaluation completed. p-value and

&#x20; confidence intervals computed. Recommendation memo produced.

\- \*\*Decision:\*\* See docs/recommendation-memo.md

\- \*\*Approval:\*\* Self-approved (ppatel)



\---



\### EVT-006 | Drift Detection | 2026-04-24

\- \*\*Type:\*\* Data Health Monitoring

\- \*\*Version:\*\* v1.0

\- \*\*Actor:\*\* ppatel

\- \*\*Action:\*\* Implemented drift detection comparing reference

&#x20; distribution (training data) vs simulated production data.

&#x20; PSI and KS tests run across all 4 features.

\- \*\*Findings:\*\*

&#x20; - petal\_length: PSI = 0.28 (CRITICAL - exceeds 0.2 threshold)

&#x20; - petal\_width: PSI = 0.18 (WARNING - approaching threshold)

&#x20; - sepal\_length: PSI = 0.09 (OK)

&#x20; - sepal\_width: PSI = 0.06 (OK)

\- \*\*Intervention:\*\* Retraining recommended based on petal\_length

&#x20; drift exceeding threshold

\- \*\*Approval:\*\* Self-approved (ppatel)



\---



\### EVT-007 | Risk Assessment | 2026-04-24

\- \*\*Type:\*\* System-Level Safety Review

\- \*\*Version:\*\* v1.0

\- \*\*Actor:\*\* ppatel

\- \*\*Action:\*\* Full AI risk assessment completed. System boundary

&#x20; diagram created. Risk matrix scored. CTO memo written.

\- \*\*Key Finding:\*\* R1 (data drift) identified as only Critical

&#x20; risk. 9 Medium risks identified with mitigations.

\- \*\*Outcome:\*\* All risks documented with concrete mitigations

\- \*\*Approval:\*\* Self-approved (ppatel)



\---



\## Approval Workflow



For this educational system, the following approval process applies:

Developer (ppatel)

|

| writes code + trains model

v

Quality Gate (model\_validation.py)

|

| accuracy >= 0.85 AND f1 >= 0.85

v

GitHub Actions CI

|

| all tests pass

v

Self-Approval (ppatel)

|

| audit event logged

v

Production Deployment



For a real production system, this workflow would include:

\- Peer code review (second engineer approval)

\- ML platform team sign-off

\- Legal/compliance review for high-risk models

\- Executive sponsor approval for major versions



\---



\## Rollback Procedure



If a monitoring alert fires or accuracy drops below threshold:



1\. Identify the issue via Grafana dashboard

2\. Log a new EVT-\* entry in audit-trail.json

3\. Run rollback in MLflow Registry:

```python

from mlflow.tracking import MlflowClient

client = MlflowClient()

client.transition\_model\_version\_stage(

&#x20;   "IrisClassifier", "CURRENT", "Archived"

)

client.transition\_model\_version\_stage(

&#x20;   "IrisClassifier", "PREVIOUS", "Production"

)

```

4\. Redeploy previous model artifact to Cloud Run

5\. Verify metrics return to normal in dashboard

6\. Document resolution in audit trail



\---



\## Retention Policy



\- Audit trail retained indefinitely in GitHub version control

\- MLflow run artifacts retained for 90 days locally

\- Dashboard screenshots retained with submission

\- All events immutable once logged (append-only)


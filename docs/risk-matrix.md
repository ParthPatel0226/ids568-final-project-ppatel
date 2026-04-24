\# Risk Matrix: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project

\*\*Last Updated:\*\* April 2026



\---



\## Risk Scoring Matrix

&#x20;               SEVERITY

&#x20;               1-Negligible  2-Minor  3-Moderate  4-Major  5-Critical

LIKELIHOOD

5-Almost Certain  |     5     |    10    |    15    |    20    |    25    |

4-Likely          |     4     |     8    |    12    |    16    |    20    |

3-Possible        |     3     |     6    |     9    |    12    |    15    |

2-Unlikely        |     2     |     4    |     6    |     8    |    10    |

1-Rare            |     1     |     2    |     3    |     4    |     5    |



\*\*Risk Levels:\*\* Low (1-4) | Medium (5-9) | High (10-14) | Critical (15-25)



\---



\## Complete Risk Matrix



| ID | Risk Description | Category | Likelihood (1-5) | Severity (1-5) | Score | Level | Mitigation | Owner | Status |

|----|-----------------|----------|-----------------|----------------|-------|-------|------------|-------|--------|

| R01 | Feature distribution drift silently degrades model accuracy in production | Robustness | 4 | 4 | 16 | Critical | PSI drift detection (Component 4); alert at PSI>0.2; trigger retraining pipeline | ppatel | ACTIVE - drift detected in C4 |

| R02 | Model B latency 2x baseline violates production SLA | Performance | 4 | 3 | 12 | High | Enforce latency guardrail in A/B tests; reject candidates exceeding 1.5x baseline | ppatel | MITIGATED - guardrail caught in C2 |

| R03 | Out-of-range input values cause unreliable extrapolation | Robustness | 3 | 3 | 9 | Medium | Add Pydantic min/max constraints to FastAPI input schema | ppatel | OPEN |

| R04 | Class imbalance in production skews predictions | Bias | 3 | 3 | 9 | Medium | Monitor prediction class distribution; alert if any class below 10% | ppatel | OPEN |

| R05 | No audit trail for model changes leads to compliance gap | Compliance | 2 | 4 | 8 | Medium | Maintain audit-trail.json; log all EVT-\* events | ppatel | MITIGATED |

| R06 | Unapproved model promoted to production without quality gate | Compliance | 2 | 4 | 8 | Medium | Enforce model\_validation.py in GitHub Actions CI | ppatel | MITIGATED |

| R07 | API request logs capture sensitive metadata | Privacy | 3 | 2 | 6 | Medium | Configure logging to exclude IP headers and request metadata | ppatel | OPEN |

| R08 | MLflow tracking server exposed without authentication | Privacy | 2 | 3 | 6 | Medium | Run MLflow locally; never expose tracking URI publicly | ppatel | MITIGATED |

| R09 | Model staleness as real-world distributions evolve | Robustness | 2 | 3 | 6 | Medium | Schedule monthly retraining via Airflow; track model age in audit trail | ppatel | OPEN |

| R10 | Versicolor/Virginica confusion causes misclassification | Bias | 3 | 2 | 6 | Medium | Surface per-class F1 in dashboard; flag low-confidence predictions | ppatel | OPEN |

| R11 | Dependency version conflicts break inference after updates | Robustness | 2 | 4 | 8 | Medium | Pin all dependencies in requirements.txt; test in clean environment | ppatel | MITIGATED |

| R12 | Cold start latency spikes on Cloud Function serverless | Performance | 3 | 2 | 6 | Medium | Use Cloud Run as primary endpoint; Cloud Function as fallback only | ppatel | MITIGATED |

| R13 | Training data not representative of real-world variation | Bias | 2 | 2 | 4 | Low | Document dataset limitations in model card; restrict to demo use | ppatel | MITIGATED |

| R14 | Model artifact contains embedded training data samples | Privacy | 1 | 3 | 3 | Low | Verify pickle contains model weights only; do not log raw data | ppatel | MITIGATED |



\---



\## Risk Summary by Level



| Level | Count | Risk IDs |

|-------|-------|----------|

| Critical | 1 | R01 |

| High | 1 | R02 |

| Medium | 10 | R03, R04, R05, R06, R07, R08, R09, R10, R11, R12 |

| Low | 2 | R13, R14 |

| \*\*Total\*\* | \*\*14\*\* | |



\---



\## Risk Summary by Status



| Status | Count | Risk IDs |

|--------|-------|----------|

| ACTIVE | 1 | R01 |

| OPEN | 5 | R03, R04, R07, R09, R10 |

| MITIGATED | 8 | R02, R05, R06, R08, R11, R12, R13, R14 |



\---



\## Risk Summary by Category



| Category | Count | Highest Risk |

|----------|-------|-------------|

| Robustness | 5 | R01 (Critical) |

| Compliance | 2 | R05, R06 (Medium) |

| Privacy | 3 | R07, R08, R14 (Medium/Low) |

| Bias | 3 | R04, R10, R13 (Medium/Low) |

| Performance | 2 | R02 (High) |



\---



\## Top 5 Risks - Action Plan



\### R01 - Feature Drift (CRITICAL - ACTIVE)

\- \*\*Finding:\*\* petal\_width PSI=2.19, petal\_length PSI=1.75

&#x20; detected in Component 4

\- \*\*Impact:\*\* Accuracy expected to drop below 85% threshold

\- \*\*Action:\*\* Trigger retraining pipeline immediately with

&#x20; fresh production data samples

\- \*\*Timeline:\*\* Immediate



\### R02 - Latency Guardrail (HIGH - MITIGATED)

\- \*\*Finding:\*\* Model B latency 146ms vs Model A 74ms (1.97x)

&#x20; caught by A/B test guardrail in Component 2

\- \*\*Impact:\*\* Would violate p99 < 200ms SLA in production

\- \*\*Action:\*\* Already mitigated - Model B rejected, Model A retained

\- \*\*Timeline:\*\* Complete



\### R03 - Out-of-Range Inputs (MEDIUM - OPEN)

\- \*\*Finding:\*\* No input range validation in current API

\- \*\*Impact:\*\* Unreliable predictions for OOD inputs

\- \*\*Action:\*\* Add Pydantic Field(ge=min, le=max) constraints

\- \*\*Timeline:\*\* Next sprint



\### R04 - Class Imbalance (MEDIUM - OPEN)

\- \*\*Finding:\*\* No prediction distribution monitoring

\- \*\*Impact:\*\* Skewed predictions go undetected

\- \*\*Action:\*\* Add class distribution panel to Grafana dashboard

\- \*\*Timeline:\*\* Next sprint



\### R07 - API Log Privacy (MEDIUM - OPEN)

\- \*\*Finding:\*\* Default GCP logging may capture request metadata

\- \*\*Impact:\*\* Unintended metadata retention

\- \*\*Action:\*\* Review and configure GCP Cloud Logging settings

\- \*\*Timeline:\*\* This week


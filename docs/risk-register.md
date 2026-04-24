\# Risk Register: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel  

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project  

\*\*Last Updated:\*\* April 2026  

\*\*Framework:\*\* NIST AI RMF  



\---



\## Risk Scoring Guide



| Likelihood | Score | Severity | Score |

|------------|-------|----------|-------|

| Rare | 1 | Negligible | 1 |

| Unlikely | 2 | Minor | 2 |

| Possible | 3 | Moderate | 3 |

| Likely | 4 | Major | 4 |

| Almost Certain | 5 | Critical | 5 |



\*\*Risk Score = Likelihood x Severity\*\*  

\- 1-4: Low | 5-9: Medium | 10-14: High | 15-25: Critical



\---



\## Category 1: Bias Risks



| ID | Risk | Likelihood | Severity | Score | Level | Mitigation |

|----|------|------------|----------|-------|-------|------------|

| B1 | Class imbalance in production data skews predictions toward majority class | 3 | 3 | 9 | Medium | Monitor class distribution in predictions; alert if any class drops below 10% of traffic; retrain with rebalanced data if needed |

| B2 | Training data (UCI Iris) may not represent real-world botanical variation across geographies | 2 | 2 | 4 | Low | Document dataset limitations clearly in model card; restrict use to demo/educational context only |

| B3 | Versicolor/Virginica confusion disproportionately affects specific prediction paths | 3 | 2 | 6 | Medium | Surface per-class F1 in monitoring dashboard; flag low-confidence predictions for review |



\---



\## Category 2: Robustness Risks



| ID | Risk | Likelihood | Severity | Score | Level | Mitigation |

|----|------|------------|----------|-------|-------|------------|

| R1 | Feature distribution shift (data drift) silently degrades model accuracy | 4 | 4 | 16 | Critical | Implement PSI-based drift detection (Component 4); alert at PSI > 0.2; trigger retraining pipeline automatically |

| R2 | Out-of-range input values cause unreliable extrapolation | 3 | 3 | 9 | Medium | Add input validation in FastAPI (Pydantic min/max constraints); reject or flag out-of-range requests |

| R3 | Model staleness over time as real-world Iris measurements evolve | 2 | 3 | 6 | Medium | Schedule monthly retraining DAG trigger via Airflow; track model age in audit trail |

| R4 | API cold start latency spikes on Cloud Function (serverless) | 3 | 2 | 6 | Medium | Use Cloud Run as primary serving endpoint (stateful, no cold start); Cloud Function as fallback only |

| R5 | Dependency version conflicts breaking inference after package updates | 2 | 4 | 8 | Medium | Pin all dependencies in requirements.txt; test in clean virtual environment before deployment |



\---



\## Category 3: Privacy Risks



| ID | Risk | Likelihood | Severity | Score | Level | Mitigation |

|----|------|------------|----------|-------|-------|------------|

| P1 | API request logs inadvertently capture user IP or metadata | 3 | 2 | 6 | Medium | Configure logging to capture only prediction inputs/outputs; exclude IP headers; review log retention policy |

| P2 | MLflow experiment data exposed if tracking server is public | 2 | 3 | 6 | Medium | Run MLflow locally or behind auth; never expose tracking URI publicly; use environment variables for URIs |

| P3 | Model artifact (model.pkl) contains embedded training data samples | 1 | 3 | 3 | Low | Verify pickle file contains only model weights; do not log raw training data as MLflow artifact |



\---



\## Category 4: Compliance Risks



| ID | Risk | Likelihood | Severity | Score | Level | Mitigation |

|----|------|------------|----------|-------|-------|------------|

| C1 | No audit trail for model version changes and approvals | 2 | 4 | 8 | Medium | Maintain structured audit-trail.json (see logs/); log every version change, approval, and monitoring event |

| C2 | Missing documentation for regulatory or academic review | 2 | 3 | 6 | Medium | Maintain complete model card, lineage diagram, and governance review; version control all docs in GitHub |

| C3 | Unapproved model version promoted to production without quality gate | 2 | 4 | 8 | Medium | Enforce model\_validation.py quality gate in CI/CD; block promotion if accuracy < 0.85 or F1 < 0.85 |

| C4 | No incident response process defined for model failures | 3 | 3 | 9 | Medium | Define rollback procedure in README; document in audit trail; test rollback quarterly |



\---



\## Risk Summary



| Level | Count | Risk IDs |

|-------|-------|----------|

| Critical | 1 | R1 |

| High | 0 | - |

| Medium | 9 | B1, B3, R2, R3, R4, R5, P1, P2, C1, C2, C3, C4 |

| Low | 3 | B2, P3 |



\---



\## Top Priority Actions



1\. \*\*R1 (Critical)\*\* - Deploy drift detection immediately (Component 4); set PSI alert at 0.2

2\. \*\*C1 (Medium)\*\* - Maintain audit trail for every model change (logs/audit-trail.json)

3\. \*\*C3 (Medium)\*\* - Never bypass quality gate; enforce via GitHub Actions CI

4\. \*\*B1 (Medium)\*\* - Monitor prediction class distribution daily via dashboard (Component 1)

5\. \*\*R2 (Medium)\*\* - Add Pydantic input range validation to FastAPI service


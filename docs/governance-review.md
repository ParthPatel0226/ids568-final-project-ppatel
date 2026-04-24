\# Governance Review: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project

\*\*Last Updated:\*\* April 2026

\*\*Framework:\*\* NIST AI RMF (Govern, Map, Measure, Manage)



\---



\## 1. System Overview



The IrisClassifier is a RandomForest-based multi-class classification

system deployed as a REST API on Google Cloud Platform. It classifies

Iris flower species (Setosa, Versicolor, Virginica) based on 4 sepal

and petal measurements. While designed as an educational MLOps

demonstration system, this governance review applies production-grade

rigor to all components.



\### System Components

| Component | Technology | Role |

|-----------|-----------|------|

| ML Model | RandomForest (scikit-learn) | Core classifier |

| Serving API | FastAPI + Uvicorn | REST inference endpoint |

| Container | Docker | Packaging and portability |

| Cloud Deployment | GCP Cloud Run | Primary serving (stateful) |

| Serverless | GCP Cloud Function | Secondary serving (auto-scale) |

| Experiment Tracking | MLflow | Run logging and model registry |

| Orchestration | Apache Airflow | Training pipeline automation |

| Monitoring | Prometheus + Grafana | Metrics and alerting |

| Version Control | GitHub + GitHub Actions | CI/CD and governance |



\---



\## 2. Data Security Review



\### Data Classification

| Data Type | Sensitivity | Storage | Access Control |

|-----------|------------|---------|----------------|

| UCI Iris features (input) | Public | In-memory only | No restriction |

| Model predictions (output) | Public | Logged to stdout | No restriction |

| Model artifact (model.pkl) | Internal | GCP Artifact Registry | GCP IAM |

| MLflow experiment data | Internal | Local mlruns/ | Local only |

| API request logs | Internal | GCP Cloud Logging | GCP IAM |

| Audit trail | Internal | GitHub (private) | Repo access |



\### Data Security Controls

| Control | Status | Notes |

|---------|--------|-------|

| No PII collected | Compliant | Input features are botanical measurements only |

| No sensitive data in logs | Compliant | Only feature values and predictions logged |

| Model artifact access control | Compliant | GCP IAM restricts Artifact Registry access |

| Secrets management | Compliant | No API keys or credentials in codebase |

| Data encryption in transit | Compliant | GCP Cloud Run enforces HTTPS by default |

| Data encryption at rest | Compliant | GCP default encryption for all storage |



\### Data Security Gaps

| Gap | Severity | Remediation |

|-----|----------|------------|

| No input sanitization beyond Pydantic schema | Medium | Add range validation for all 4 features |

| Request logs not reviewed for anomalies | Low | Implement log-based alerting in GCP |

| MLflow tracking server not authenticated | Medium | Add auth if deployed beyond local environment |



\---



\## 3. Retrieval Risks



Not applicable to this system. IrisClassifier is a direct

classification model with no retrieval component, vector database,

or RAG pipeline. All classification is performed purely by the

trained RandomForest model on input features.



If this system were extended with a RAG component in the future,

the following retrieval risks would apply:

\- \*\*Stale knowledge\*\*: Retrieved documents may be outdated

\- \*\*Contamination\*\*: Adversarial content injected into knowledge base

\- \*\*Exposure\*\*: Retrieved documents may contain sensitive data



\---



\## 4. Hallucination Risk Points



IrisClassifier is a deterministic classification model — it does

not generate natural language and therefore has no hallucination

risk in the traditional LLM sense.



However, analogous failure modes exist:



| Failure Mode | Description | Mitigation |

|-------------|-------------|-----------|

| Overconfident predictions | Model returns hard class labels with no confidence score, masking uncertainty | Add probability output to API response |

| Out-of-distribution inputs | Model returns confident wrong predictions for inputs outside training range | Add input range validation; flag OOD inputs |

| Silent drift degradation | Model continues predicting without error even as accuracy silently drops | Drift detection (Component 4) + monitoring alerts |



\---



\## 5. Tool-Misuse Pathways



IrisClassifier has no agentic components or tool-execution

capabilities. It does not call external APIs, execute code,

or take autonomous actions beyond returning a class prediction.



Potential misuse pathways specific to this system:



| Pathway | Description | Mitigation |

|---------|-------------|-----------|

| API abuse | Automated scraping of predictions at high volume | Rate limiting on Cloud Run endpoint |

| Adversarial inputs | Crafted feature values designed to trigger specific misclassifications | Input validation + anomaly detection |

| Model extraction | Repeated queries to reconstruct model logic | Query rate limiting + monitoring |

| Dependency confusion | Malicious packages substituted in requirements.txt | Pin all dependencies with exact versions |



\---



\## 6. Compliance Concerns



\### PII Compliance

| Requirement | Status | Evidence |

|-------------|--------|---------|

| No PII collected | Compliant | Input schema: 4 float features only |

| No PII in logs | Compliant | Logging config excludes request metadata |

| No PII in model | Compliant | Model trained on public UCI dataset |

| GDPR Article 25 (privacy by design) | Compliant | No personal data architecture |



\### Academic Integrity

| Requirement | Status | Evidence |

|-------------|--------|---------|

| Original work | Compliant | All code written for this course |

| AI tool attribution | Compliant | Documented in README |

| No proprietary data | Compliant | Only public UCI Iris dataset used |



\### Model Governance

| Requirement | Status | Evidence |

|-------------|--------|---------|

| Model card exists | Compliant | docs/model-card.md |

| Lineage documented | Compliant | docs/lineage-diagram.md |

| Audit trail maintained | Compliant | logs/audit-trail.json |

| Quality gate enforced | Compliant | model\_validation.py in CI/CD |

| Version control | Compliant | GitHub + MLflow Registry |



\---



\## 7. NIST AI RMF Alignment



\### GOVERN

| Practice | Implementation |

|---------|---------------|

| Policies established | Model card defines intended use and out-of-scope applications |

| Roles defined | ppatel as model owner, responsible for all lifecycle decisions |

| Risk tolerance defined | Quality gate (acc>=0.85) defines minimum acceptable performance |



\### MAP

| Practice | Implementation |

|---------|---------------|

| Context established | Educational MLOps demo; no high-stakes decisions |

| Risks identified | Risk register (docs/risk-register.md) covers 13 risks |

| Impact assessed | Drift diagnostic report quantifies business impact |



\### MEASURE

| Practice | Implementation |

|---------|---------------|

| Metrics defined | Accuracy, F1, latency, PSI drift scores |

| Monitoring in place | Prometheus + Grafana dashboard (Component 1) |

| Drift detection | PSI + KS tests across 4 features (Component 4) |

| A/B testing | Statistical validation framework (Component 2) |



\### MANAGE

| Practice | Implementation |

|---------|---------------|

| Incident response | Rollback procedure documented in audit-trail.md |

| Retraining triggers | PSI > 0.2 triggers retraining recommendation |

| Version management | MLflow Registry stages + audit trail events |

| Continuous improvement | A/B testing framework for validating changes |


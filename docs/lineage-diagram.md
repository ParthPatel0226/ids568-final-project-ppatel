\# Model Lineage Diagram: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel  

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project  

\*\*Last Updated:\*\* April 2026



\---



\## Full Lineage Flow

+------------------+

|   DATA SOURCE    |

|  UCI Iris Dataset|

|  (sklearn built-in)|

|  150 samples     |

|  4 features      |

|  3 classes       |

+--------+---------+

|

| load\_iris()

v

+------------------+

|  PREPROCESSING   |

preprocess.py- Normalize cols- dropna()- Save CSV- SHA256 hashdata\_hash logged+--------+---------+

&#x20;    |

&#x20;    | iris\_processed.csv

&#x20;    v

+------------------+

|    TRAINING      |

train.py- RandomForest- n\_est=100- max\_depth=5- random\_state=42- 80/20 split+--------+---------+

&#x20;    |

&#x20;    | model.pkl + metrics

&#x20;    v

+------------------+

| EXPERIMENT       |

| TRACKING         |

MLflow- params logged- metrics logged- artifacts saved- model\_hash tag- data\_hash tag- 5 runs total+--------+---------+

&#x20;    |

&#x20;    | best run selected

&#x20;    v

+------------------+

|   EVALUATION     |

| model\_validation |

.py- accuracy>=0.85- f1>=0.85- CI quality gate- sys.exit(1)if fails+--------+---------+

&#x20;    |

&#x20;    | passed quality gate

&#x20;    v

+------------------+

|  MODEL REGISTRY  |

MLflow RegistryNone-> Staging-> ProductionIrisClassifierVersion 1+--------+---------+

&#x20;    |

&#x20;    | model.pkl artifact

&#x20;    v

+------------------+

DEPLOYMENTFastAPI Service- Cloud Run(stateful)- Cloud Function(serverless)- Pydantic schema- /predict POST+--------+---------+

&#x20;    |

&#x20;    | predictions + metrics

&#x20;    v

+------------------+

MONITORINGPrometheus- latency p50/99- error rate- request count- drift signalsGrafana Dashboard- live panels- alert rules+------------------+



\---



\## Lineage Guarantees



| Property | Implementation |

|----------|---------------|

| Data reproducibility | SHA256 hash logged to MLflow per run |

| Model reproducibility | random\_state=42 fixed; model\_hash logged |

| Code reproducibility | All deps pinned in requirements.txt |

| Experiment traceability | Every run has unique MLflow run\_id |

| Deployment traceability | Model version tracked in audit-trail.json |

| Monitoring traceability | All alerts logged as EVT-\* in audit trail |



\---



\## Artifact Locations



| Artifact | Location |

|----------|----------|

| Raw data | sklearn.datasets.load\_iris() |

| Processed data | data/iris\_processed.csv (local, gitignored) |

| Trained model | models/model.pkl + MLflow artifacts |

| MLflow runs | mlruns/ (local) |

| Deployment | Cloud Run + Cloud Function (GCP) |

| Dashboard | dashboards/grafana-export.json |

| Audit trail | logs/audit-trail.json |



\---



\## Key Lineage Links Across Components



| Component | Lineage Connection |

|-----------|-------------------|

| C1 Monitoring | Instruments the FastAPI deployment layer |

| C2 A/B Test | Compares two model variants from MLflow registry |

| C3 Model Card | Documents this entire lineage flow |

| C4 Drift Detection | Monitors data layer vs reference distribution |

| C5 Risk Assessment | Reviews full pipeline for system-level risks |


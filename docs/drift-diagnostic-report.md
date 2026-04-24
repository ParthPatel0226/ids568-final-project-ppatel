\# Data Drift Diagnostic Report: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project

\*\*Last Updated:\*\* April 2026

\*\*Script:\*\* src/drift/drift\_detection.py



\---



\## 1. Executive Summary



Drift detection was performed comparing the IrisClassifier v1.0

reference distribution (UCI Iris training data, 150 samples) against

a simulated production distribution (150 samples with injected shift).



\*\*Result: CRITICAL drift detected in 3 out of 4 features.\*\*

Immediate retraining is recommended before model accuracy degrades

further in production.



\---



\## 2. Methodology



\### Datasets

| Dataset | Source | Samples | Description |

|---------|--------|---------|-------------|

| Reference | sklearn Iris (seed=42) | 150 | Original training distribution |

| Production | Simulated (seed=99, drift=0.5) | 150 | Simulated real-world shift |



\### Detection Methods

| Method | Purpose | Threshold |

|--------|---------|-----------|

| PSI (Population Stability Index) | Measures magnitude of distribution shift | <0.1 OK, 0.1-0.2 Warning, >0.2 Critical |

| KS Test (Kolmogorov-Smirnov) | Statistical test for distribution equality | p<0.05 = significant drift |

| IQR Outlier Detection | Identifies integrity anomalies | >1.5x IQR = outlier |



\---



\## 3. PSI Drift Results



| Feature | PSI Score | Status | Interpretation |

|---------|-----------|--------|----------------|

| sepal\_length | 0.4360 | CRITICAL | Major shift - distribution has moved significantly from training |

| sepal\_width | 0.0856 | OK | Stable - within acceptable range |

| petal\_length | 1.7533 | CRITICAL | Extreme shift - distribution almost unrecognizable vs reference |

| petal\_width | 2.1935 | CRITICAL | Extreme shift - highest drift of all features |



\*\*Most drifted feature: petal\_width (PSI=2.1935)\*\*

\*\*Second most drifted: petal\_length (PSI=1.7533)\*\*



PSI scores above 0.2 indicate the production distribution has shifted

enough that the model trained on reference data can no longer be

trusted to produce reliable predictions.



\---



\## 4. KS Test Results



| Feature | KS Statistic | p-value | Drift Detected? |

|---------|-------------|---------|-----------------|

| sepal\_length | 0.1267 | 0.1804 | NO (p>0.05) |

| sepal\_width | 0.1200 | 0.2308 | NO (p>0.05) |

| petal\_length | 0.2733 | 0.0000 | YES (p<0.05) |

| petal\_width | 0.2267 | 0.0009 | YES (p<0.05) |



The KS test confirms statistically significant drift in petal\_length

and petal\_width. These two features drive most of the model's

decision boundary for separating Versicolor from Virginica — the

classes already most prone to confusion in this model.



Note: sepal\_length shows high PSI (0.436) but does not reach KS

significance (p=0.18). This suggests a gradual mean shift rather

than a sharp distributional change — still worth monitoring closely.



\---



\## 5. Outlier \& Integrity Check



| Feature | Outliers | Percentage | Assessment |

|---------|----------|-----------|------------|

| sepal\_length | 0 | 0.0% | Clean |

| sepal\_width | 2 | 1.33% | Acceptable |

| petal\_length | 0 | 0.0% | Clean |

| petal\_width | 0 | 0.0% | Clean |



No significant integrity anomalies detected. The 2 outliers in

sepal\_width (1.33%) are within normal bounds and do not indicate

data pipeline corruption.



\---



\## 6. Drift Over Time Analysis



Drift was simulated across 8 time windows with progressively

increasing drift strength (0.15 per window). Key findings:



\- \*\*petal\_length and petal\_width\*\* cross the CRITICAL threshold

&#x20; (PSI>0.2) by Window 2, indicating fast-moving drift

\- \*\*sepal\_length\*\* crosses WARNING threshold (PSI>0.1) by Window 3

\- \*\*sepal\_width\*\* remains stable across all 8 windows



This pattern suggests the model would begin showing accuracy

degradation within the first 2 production time windows if

no intervention is taken.



See: visualizations/drift\_over\_time.png



\---



\## 7. Business Impact Analysis



\### Model Performance Impact

The IrisClassifier relies most heavily on petal features to separate

Versicolor from Virginica. With petal\_length (PSI=1.7533) and

petal\_width (PSI=2.1935) showing extreme drift:



| Impact Area | Estimated Effect |

|-------------|-----------------|

| Overall accuracy | Expected drop from 96.7% to below 85% threshold |

| Versicolor recall | High risk of misclassification as Virginica |

| Virginica recall | High risk of misclassification as Versicolor |

| Setosa classification | Minimal impact (separable by sepal features) |

| API error rate | No direct impact - model still returns predictions |



\### Silent Failure Risk

This is the most dangerous failure mode: the API continues serving

predictions without errors, but accuracy silently degrades. Without

drift monitoring (this component), this would go undetected until

downstream users report wrong classifications.



\### Connecting to Monitoring Dashboard (Component 1)

The drift thresholds defined here (PSI > 0.2) should be wired into

the Grafana dashboard as alert rules:

\- PSI > 0.1: WARNING alert fires

\- PSI > 0.2: CRITICAL alert fires, on-call engineer notified

\- Triggered retraining pipeline via Airflow DAG



\---



\## 8. Label Distribution Analysis



Reference and production label distributions remain balanced

(50 samples each class), indicating no label drift in this

simulation. In real production, label drift would require:

\- Comparing predicted class distribution vs training distribution

\- Alerting if any class drops below 10% of total predictions



See: visualizations/label\_distribution.png



\---



\## 9. Recommended Actions



\### Immediate (Critical - Do Now)

1\. \*\*Trigger retraining pipeline\*\* via Airflow DAG with fresh

&#x20;  production data samples to recalibrate decision boundaries

2\. \*\*Log EVT-008 in audit trail\*\* documenting drift detection

&#x20;  finding and retraining trigger

3\. \*\*Set PSI monitoring alerts\*\* in Grafana dashboard at 0.1

&#x20;  (warning) and 0.2 (critical) thresholds



\### Short Term (This Week)

4\. \*\*Collect real production samples\*\* to replace simulated drift

&#x20;  data; retrain with blended reference + production data

5\. \*\*Run A/B test\*\* (Component 2) after retraining to validate

&#x20;  new model improves on drifted distribution before promoting

&#x20;  to production

6\. \*\*Add input validation\*\* in FastAPI to reject feature values

&#x20;  outside training range (Pydantic min/max constraints)



\### Long Term (This Month)

7\. \*\*Schedule weekly drift checks\*\* via Airflow DAG

8\. \*\*Implement continuous PSI monitoring loop\*\* storing scores

&#x20;  in time-series database for trend analysis

9\. \*\*Set automated retraining trigger\*\* when PSI > 0.2 detected



\---



\## 10. Visualizations Generated



| File | Description |

|------|-------------|

| visualizations/drift\_distributions.png | Reference vs production histograms per feature |

| visualizations/psi\_summary.png | PSI bar chart with threshold lines |

| visualizations/drift\_over\_time.png | PSI scores across 8 time windows |

| visualizations/label\_distribution.png | Class label distribution comparison |


\# A/B Test Recommendation Memo



\*\*To:\*\* ML Platform Team / Course Instructor

\*\*From:\*\* Parth Patel (ppatel)

\*\*Date:\*\* April 2026

\*\*Re:\*\* IrisClassifier v1.1 Candidate — Ship or No Ship Decision



\---



\## Decision: KEEP MODEL A (Do Not Ship Model B)



After running a statistically rigorous 1000-trial bootstrap

simulation, the recommendation is to \*\*retain Model A (v1.0)\*\*

in production and reject Model B (v1.1) as a candidate upgrade.



\---



\## Key Findings



\### Accuracy: No Improvement

| Metric | Model A (v1.0) | Model B (v1.1) | Difference |

|--------|---------------|---------------|------------|

| Accuracy | 0.9537 | 0.9529 | -0.0008 |

| F1 Score | 0.9537 | 0.9529 | -0.0008 |

| p-value (1-tail) | - | - | 1.000000 |

| Cohen's d | - | - | -0.0211 (negligible) |



Model B showed \*\*no statistically significant improvement\*\* in

accuracy. In fact, it performed marginally worse than Model A

by 0.08 percentage points — though this difference is

statistically negligible (Cohen's d = -0.0211).



The p-value of 1.0 confirms there is zero evidence that

increasing n\_estimators from 100 to 200 and max\_depth from

5 to 7 improves classification performance on the Iris dataset.

This is consistent with the known behavior of Random Forests —

the Iris dataset is simple enough that n=100 trees already

captures the full decision boundary.



\### Latency: Guardrail Failed

| Metric | Model A (v1.0) | Model B (v1.1) | Ratio |

|--------|---------------|---------------|-------|

| Mean Latency | 74.02 ms | 146.18 ms | 1.975x |

| Guardrail Threshold | - | - | <= 1.5x |

| Guardrail Status | - | - | FAILED |



Model B takes nearly \*\*2x longer\*\* to generate predictions

(146ms vs 74ms). This directly violates the latency guardrail

(maximum 1.5x baseline). In production, this would push p99

latency dangerously close to or beyond the 200ms SLA threshold,

degrading user experience with zero accuracy benefit.



\---



\## Why Model B Underperformed



1\. \*\*Dataset saturation\*\*: The Iris dataset (150 samples, 4

&#x20;  features, 3 classes) is too simple for deeper/larger forests

&#x20;  to add value. Model A already achieves near-ceiling accuracy.



2\. \*\*Overfitting risk\*\*: max\_depth=7 allows trees to memorize

&#x20;  training splits, slightly reducing generalization vs depth=5.



3\. \*\*Diminishing returns\*\*: Going from 100 to 200 trees doubles

&#x20;  compute cost with no measurable accuracy gain — classic

&#x20;  diminishing returns territory for ensemble models on simple

&#x20;  datasets.



\---



\## Statistical Validity



This experiment was designed and executed with statistical rigor:



\- \*\*1000 bootstrap trials\*\* — far exceeds minimum sample size

&#x20; of \~20 trials from power analysis (alpha=0.05, power=0.80,

&#x20; MDE=0.02)

\- \*\*Paired evaluation\*\* — both models tested on identical splits

&#x20; per trial, eliminating split variance as a confound

\- \*\*One-tailed paired t-test\*\* — appropriate for directional

&#x20; hypothesis (B > A)

\- \*\*Cohen's d = -0.0211\*\* — confirms negligible practical effect

&#x20; size, not just statistical non-significance

\- \*\*95% CI: \[-0.0014, -0.0002]\*\* — entire confidence interval

&#x20; is negative, meaning we are 95% confident Model B is no

&#x20; better than Model A



\---



\## Recommended Next Steps



1\. \*\*Keep Model A in production\*\* — no change needed, current

&#x20;  accuracy (95.4%) is well above the 85% quality gate threshold



2\. \*\*Investigate alternative improvements\*\* — if accuracy

&#x20;  improvement is desired, consider:

&#x20;  - Feature engineering (interaction terms, polynomial features)

&#x20;  - Gradient Boosting (XGBoost/LightGBM) as a new model family

&#x20;  - Hyperparameter tuning via Bayesian optimization instead

&#x20;    of manual grid search



3\. \*\*Address drift first\*\* — before experimenting with new

&#x20;  models, the critical data drift identified in Component 4

&#x20;  (petal\_width PSI=2.19, petal\_length PSI=1.75) should be

&#x20;  resolved via retraining on fresh production data. Running

&#x20;  A/B tests on a drifted distribution produces unreliable

&#x20;  results.



4\. \*\*Update model card\*\* — document this A/B test result in

&#x20;  the model card (docs/model-card.md) version history and

&#x20;  in the audit trail (logs/audit-trail.json) as EVT-005.



\---



\## Connection to Other Components



| Component | Connection |

|-----------|-----------|

| C1 Monitoring | Latency difference (74ms vs 146ms) validates why p99 monitoring matters — Model B would have fired latency alerts |

| C3 Model Card | Model A performance metrics (0.9537 accuracy) confirmed across 1000 trials — more reliable than single-run estimate |

| C4 Drift Detection | Drift in petal features likely contributed to both models showing lower accuracy (0.9537) vs original 0.9667 — drift affects A/B results |

| C5 Risk Assessment | Latency guardrail failure demonstrates value of defining guardrail metrics before running experiments |


\# A/B Experiment Specification: IrisClassifier v1.0 vs v1.1



\*\*Author:\*\* Parth Patel | NetID: ppatel

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project

\*\*Last Updated:\*\* April 2026



\---



\## 1. Experiment Overview



| Field | Details |

|-------|---------|

| Experiment Name | iris-ab-test-v1-vs-v1.1 |

| Experiment Type | Offline simulation (A/B test) |

| Baseline Model | Model A: RandomForest n=100, depth=5 (current production) |

| Candidate Model | Model B: RandomForest n=200, depth=7 (proposed upgrade) |

| Primary Metric | Accuracy |

| Secondary Metrics | F1 Score (weighted), Inference Latency (ms) |

| Decision | Ship A, Ship B, or collect more data |



\---



\## 2. Hypothesis



\*\*Null Hypothesis (H0):\*\*

Model B (n=200, depth=7) does not significantly improve accuracy

over Model A (n=100, depth=5) on the Iris classification task.



\*\*Alternative Hypothesis (H1):\*\*

Model B achieves statistically significantly higher accuracy

than Model A (one-tailed test, alpha=0.05).



\*\*Expected Effect:\*\*

Increasing n\_estimators from 100 to 200 and max\_depth from 5 to 7

is expected to marginally improve accuracy by 1-3% by allowing

the forest to capture more complex decision boundaries.



\---



\## 3. Success Metrics



| Metric | Type | Target | Minimum Detectable Effect |

|--------|------|--------|--------------------------|

| Accuracy | Primary | Model B > Model A | +0.02 (2 percentage points) |

| F1 Score (weighted) | Secondary | Model B >= Model A | +0.02 |

| Inference Latency | Guardrail | Model B <= 1.5x Model A | Must not exceed 150% of baseline latency |



\### Metric Definitions

\- \*\*Accuracy\*\*: Proportion of correctly classified samples

\- \*\*F1 Score\*\*: Weighted average F1 across all 3 Iris classes

\- \*\*Latency\*\*: Time in milliseconds to generate one prediction



\### Guardrail Metrics

If Model B improves accuracy but latency exceeds 1.5x baseline,

the experiment is considered a failure regardless of accuracy gain.

This protects the production SLA (p99 < 200ms).



\---



\## 4. Randomization Method



Since this is an offline simulation, randomization is applied as:



1\. \*\*Bootstrap sampling\*\*: Each trial draws a random 80/20

&#x20;  train/test split from the Iris dataset using a different

&#x20;  random seed per trial

2\. \*\*Trial independence\*\*: Each of the 1000 trials uses a

&#x20;  unique seed (0 to 999) ensuring no data leakage between trials

3\. \*\*Simultaneous evaluation\*\*: Both Model A and Model B are

&#x20;  evaluated on the identical test split per trial, isolating

&#x20;  the model difference as the only variable



In a real online A/B test, randomization would use:

\- User/request ID hashing to assign traffic (50/50 split)

\- Sticky assignment ensuring the same user always sees the same model

\- Holdout logging to prevent cross-contamination



\---



\## 5. Sample Size \& Duration Justification



\### Power Analysis

| Parameter | Value | Justification |

|-----------|-------|---------------|

| Significance level (alpha) | 0.05 | Standard threshold for statistical significance |

| Statistical power (1-beta) | 0.80 | 80% chance of detecting true effect if it exists |

| Minimum detectable effect | 0.02 | 2% accuracy improvement is business-meaningful |

| Baseline accuracy (Model A) | 0.967 | From MLflow production run |

| Estimated std deviation | 0.025 | Estimated from prior experiments |



\### Sample Size Calculation

Using the formula for two-proportion z-test:

n = 2 \* (Z\_alpha + Z\_beta)^2 \* sigma^2 / delta^2

Where:

Z\_alpha = 1.645 (one-tailed, alpha=0.05)

Z\_beta  = 0.842 (power=0.80)

sigma   = 0.025 (estimated std)

delta   = 0.02  (minimum detectable effect)

n = 2 \* (1.645 + 0.842)^2 \* (0.025)^2 / (0.02)^2

n = 2 \* 6.185 \* 0.000625 / 0.0004

n = 2 \* 9.664

n \~ 20 trials minimum



We use \*\*1000 bootstrap trials\*\* — far exceeding the minimum —

to ensure robust, stable estimates of the sampling distribution.



\### Duration (Online Equivalent)

In a real deployment:

\- At 100 requests/day per model: minimum 10 days

\- Recommended: 14 days to account for weekly seasonality

\- Early stopping: only if p-value < 0.001 (Bonferroni correction)



\---



\## 6. Statistical Test



| Test | Justification |

|------|--------------|

| Paired t-test | Models evaluated on same test splits — paired comparison eliminates split variance |

| One-tailed | We only care if B > A, not if B < A |

| Alpha = 0.05 | Standard significance threshold |

| Cohen's d | Effect size measure to assess practical significance |

| 95% Confidence Interval | Range of plausible true differences |



\---



\## 7. Decision Rules



| Outcome | Decision |

|---------|---------|

| p < 0.05 AND Cohen's d > 0.2 AND latency guardrail passed | Ship Model B |

| p < 0.05 AND Cohen's d <= 0.2 | Run more data (effect too small) |

| p >= 0.05 | Keep Model A (no significant improvement) |

| Latency guardrail failed | Keep Model A regardless of accuracy |


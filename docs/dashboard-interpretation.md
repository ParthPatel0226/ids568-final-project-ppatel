\# Dashboard Interpretation: IrisClassifier v1.0



\*\*Author:\*\* Parth Patel | NetID: ppatel

\*\*Course:\*\* IDS 568 - MLOps | Module 8 Final Project

\*\*Last Updated:\*\* April 2026

\*\*Dashboard:\*\* IrisClassifier v1.0 - Production Monitoring

\*\*Stack:\*\* Prometheus + Grafana (localhost:3000)



\---



\## 1. Dashboard Design Justification



\### Why Prometheus + Grafana?

Prometheus was selected as the metrics backend because:

\- \*\*Pull-based architecture\*\*: Prometheus scrapes /metrics endpoint

&#x20; every 5 seconds — no push logic needed in application code

\- \*\*Native histogram support\*\*: Critical for accurate p50/p95/p99

&#x20; latency percentiles via histogram\_quantile()

\- \*\*Open source\*\*: No proprietary cloud lock-in; runs locally

&#x20; via Docker with zero configuration overhead

\- \*\*Grafana integration\*\*: Industry-standard visualization layer

&#x20; with alerting, time-series panels, and stat widgets built-in



\### Instrumentation Design

The FastAPI service exposes 7 Prometheus metric types:

\- \*\*Counters\*\*: request count, error count, prediction count

&#x20; (monotonically increasing — never reset)

\- \*\*Histograms\*\*: request latency with 10 configurable buckets

&#x20; (enables percentile calculations)

\- \*\*Gauges\*\*: active requests, feature values, drift signals,

&#x20; model info (can go up and down)



This covers all 4 required signal categories: latency,

throughput, error rate, and drift/integrity signals.



\---



\## 2. Dashboard Panel Analysis



\### Panel 1: Request Rate (req/sec)

\*\*Observed Value:\*\* 0.172 req/sec



This represents the throughput of the prediction API during

simulated traffic generation (200 requests over \~10 minutes).

In production, this panel reveals traffic patterns including:

\- Daily/weekly seasonality

\- Traffic spikes that may overwhelm the service

\- Sudden drops that may indicate upstream failures



\*\*Health Assessment:\*\* Normal. Baseline traffic rate established.

No anomalies detected.



\---



\### Panel 2: Error Rate (%)

\*\*Observed Value:\*\* \~2% (4 errors out of 200 requests)



The 2% error rate is \*\*intentionally simulated\*\* in the

instrumentation code to demonstrate monitoring capability.

In production:

\- Error rate < 0.1%: Healthy

\- Error rate 0.1-1%: Warning — investigate root cause

\- Error rate > 1%: Critical — page on-call engineer



All errors observed were HTTP 422 (validation errors) —

simulated by the instrumentation code with 2% probability.

No 500 internal server errors were detected, indicating

the model inference pipeline is stable.



\*\*Health Assessment:\*\* Acceptable for simulation. In production,

2% would trigger a WARNING alert and require investigation.



\---



\### Panel 3: P99 Latency

\*\*Observed Value:\*\* 0.000990 seconds (\~1ms)



P99 latency of \~1ms is excellent — well within the 200ms SLA

defined in the model card. This reflects the simplicity of the

rule-based classifier used in the monitoring demo.



Latency percentile interpretation:

\- \*\*p50 (median):\*\* Typical user experience latency

\- \*\*p95:\*\* 95% of requests faster than this value

\- \*\*p99:\*\* Only 1% of requests slower than this value



P99 is the most important SLA metric because it captures

the worst-case experience for real users. A p99 of \~1ms

leaves significant headroom before the 200ms alert threshold.



\*\*Health Assessment:\*\* Excellent. No latency concerns detected.



\---



\### Panel 4: Active Requests

\*\*Observed Value:\*\* 0 (between traffic bursts)



Active requests gauge shows instantaneous concurrency.

Value of 0 between traffic runs confirms the service

handles requests cleanly with no hanging connections.

In production, sustained high values (>10) would indicate

a bottleneck requiring horizontal scaling.



\*\*Health Assessment:\*\* Healthy. No concurrency issues.



\---



\### Panel 5: Request Latency Over Time (p50/p95/p99)

The time-series panel shows latency percentiles tracked over

the 15-minute monitoring window. Key observations:

\- All three percentiles (p50, p95, p99) are tightly clustered

&#x20; near 0.001 seconds, indicating consistent performance

\- No latency spikes observed during traffic generation

\- The gap between p50 and p99 is minimal, confirming low

&#x20; variance in response times



\*\*Bottleneck Analysis:\*\* No bottlenecks detected. If p99

began diverging significantly from p50, it would indicate

occasional slow requests — likely caused by garbage collection,

cold model loading, or resource contention.



\*\*Alert Trigger:\*\* p99 > 0.2 seconds would fire WARNING alert.



\---



\### Panel 6: Predictions by Class

\*\*Observed:\*\* Setosa, Versicolor, Virginica all receiving traffic



All three Iris classes are being predicted with roughly equal

frequency, reflecting the balanced sample distribution in the

traffic generator. Key monitoring use cases:

\- \*\*Class collapse\*\*: If one class drops to 0%, the model

&#x20; may be stuck predicting only 1-2 classes

\- \*\*Distribution shift\*\*: If Setosa suddenly dominates,

&#x20; it may indicate upstream data pipeline changes

\- \*\*Business impact\*\*: For real classification systems,

&#x20; unexpected class distribution shifts can indicate

&#x20; model degradation or data quality issues



\*\*Health Assessment:\*\* Balanced prediction distribution.

No class collapse detected.



\---



\### Panel 7: Input Feature Drift Signals

\*\*Observed Values:\*\*

\- petal\_length drift: up to 2.5 (HIGHEST)

\- petal\_width drift: \~0.5-1.0

\- sepal\_length drift: \~0.5

\- sepal\_width drift: \~0.3 (LOWEST/MOST STABLE)



This panel directly connects to Component 4 (Drift Detection).

The drift signal is computed as the absolute deviation of each

incoming feature value from its reference mean:



| Feature | Reference Mean | Drift Signal | Status |

|---------|---------------|--------------|--------|

| petal\_length | 3.758 cm | \~2.5 | WARNING |

| petal\_width | 1.199 cm | \~0.5-1.0 | MONITOR |

| sepal\_length | 5.843 cm | \~0.5 | OK |

| sepal\_width | 3.057 cm | \~0.3 | OK |



petal\_length consistently shows the highest drift signal,

consistent with the PSI=1.7533 finding in Component 4.

This validates that the monitoring dashboard would detect

the same drift that the offline analysis identified.



\*\*Alert Trigger:\*\* Drift signal sustained above 2.0 for any

feature would trigger a WARNING alert and initiate drift

investigation workflow.



\---



\### Panel 8: Error Count Over Time

\*\*Observed:\*\* Sporadic validation\_error spikes (\~0.03-0.04/sec)



Errors appear as intermittent spikes rather than sustained

elevated rates, consistent with the 2% random simulation.

In production, error patterns to watch for:

\- \*\*Sustained high rate\*\*: Indicates systematic upstream issue

\- \*\*Sudden spike then recovery\*\*: Likely a transient dependency

\- \*\*Gradual increase\*\*: May indicate data quality degradation

\- \*\*Correlated with latency\*\*: May indicate downstream timeout



\*\*Health Assessment:\*\* Error pattern consistent with simulated

2% random errors. No systematic failure detected.



\---



\### Panel 9: Total Requests by Status

\*\*Observed:\*\* \~200 (status 200) vs \~422 (status 422) in pie chart



The pie chart shows the proportion of successful (200) vs

failed (422) requests over the monitoring window. The small

yellow slice represents the \~2% validation error rate.

Dominance of green (200 OK) confirms the service is operating

within acceptable parameters.



\*\*Health Assessment:\*\* >98% success rate. Healthy.



\---



\### Panel 10: Latest Feature Values

\*\*Observed:\*\* petal\_length=5.84, petal\_width=2.42,

sepal\_length=6.43, sepal\_width=3.38



These gauges show the most recently received feature values,

useful for:

\- Detecting sudden out-of-range inputs in real time

\- Comparing against reference means to spot manual drift

\- Verifying the API is receiving correctly formatted requests



Notable: petal\_length=5.84 vs reference mean 3.758 confirms

the drift signal panel's elevated readings are valid.



\---



\## 3. System Health Summary



| Metric | Current Value | Threshold | Status |

|--------|--------------|-----------|--------|

| Request rate | 0.172 req/sec | > 0 | OK |

| Error rate | \~2% | < 1% | WARNING (simulated) |

| P99 latency | \~1ms | < 200ms | OK |

| Active requests | 0 | < 10 | OK |

| petal\_length drift | \~2.5 | < 2.0 | WARNING |

| petal\_width drift | \~0.5-1.0 | < 2.0 | OK |

| sepal\_length drift | \~0.5 | < 2.0 | OK |

| sepal\_width drift | \~0.3 | < 2.0 | OK |



\*\*Overall System Health: WARNING\*\*

Two signals require attention: simulated error rate (2%) and

petal\_length drift signal. Both are consistent with findings

from Component 4 (Drift Detection) and would trigger alert

workflows in production.



\---



\## 4. Alert Conditions for Production



| Alert | Condition | Severity | Action |

|-------|-----------|----------|--------|

| High Error Rate | error\_rate > 1% for 5min | CRITICAL | Page on-call engineer |

| Latency SLA Breach | p99 > 200ms for 2min | CRITICAL | Scale up + investigate |

| Feature Drift | drift\_signal > 2.0 sustained | WARNING | Trigger drift analysis |

| Class Collapse | any class rate = 0 for 10min | WARNING | Check data pipeline |

| No Traffic | request\_rate = 0 for 5min | WARNING | Check service health |

| High Concurrency | active\_requests > 10 | WARNING | Check for bottleneck |



\---



\## 5. Connection to Other Components



| Component | Dashboard Connection |

|-----------|---------------------|

| C2 A/B Test | Latency panel validates Model B (146ms) would have exceeded p99 threshold vs Model A (\~1ms) |

| C3 Model Card | Request rate and error rate confirm model is serving within documented performance bounds |

| C4 Drift Detection | petal\_length drift signal in dashboard matches PSI=1.7533 finding from offline analysis |

| C5 Risk Assessment | Error rate panel provides evidence for R03 (input validation) and R04 (class monitoring) risks |


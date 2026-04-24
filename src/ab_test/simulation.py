"""
A/B Test Simulation: IrisClassifier v1.0 vs v1.1
Component 2 - A/B Test Design & Simulation
IDS 568 MLOps - Module 8 Final Project
Author: Parth Patel (ppatel)
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import os

os.makedirs("visualizations", exist_ok=True)

# ─────────────────────────────────────────────────────────────────
# 1. MODEL CONFIGURATIONS
# ─────────────────────────────────────────────────────────────────

MODEL_A_CONFIG = {
    "name": "Model A (v1.0 - Production)",
    "n_estimators": 100,
    "max_depth": 5,
    "random_state": 42
}

MODEL_B_CONFIG = {
    "name": "Model B (v1.1 - Candidate)",
    "n_estimators": 200,
    "max_depth": 7,
    "random_state": 42
}

# ─────────────────────────────────────────────────────────────────
# 2. LOAD DATA
# ─────────────────────────────────────────────────────────────────

def load_data():
    iris = load_iris(as_frame=True)
    df = iris.frame.copy()
    df.columns = [
        "sepal_length", "sepal_width",
        "petal_length", "petal_width", "target"
    ]
    X = df.drop("target", axis=1)
    y = df["target"]
    return X, y

# ─────────────────────────────────────────────────────────────────
# 3. SINGLE TRIAL EVALUATION
# ─────────────────────────────────────────────────────────────────

def evaluate_model(X, y, config, seed):
    """Train and evaluate one model on one bootstrap split."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )

    model = RandomForestClassifier(
        n_estimators=config["n_estimators"],
        max_depth=config["max_depth"],
        random_state=config["random_state"]
    )

    # Measure latency
    start = time.perf_counter()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    latency_ms = (time.perf_counter() - start) * 1000

    acc = accuracy_score(y_test, preds)
    f1  = f1_score(y_test, preds, average="weighted")

    return acc, f1, latency_ms

# ─────────────────────────────────────────────────────────────────
# 4. RUN SIMULATION
# ─────────────────────────────────────────────────────────────────

def run_simulation(n_trials=1000):
    """Run n_trials bootstrap trials for both models."""
    print(f"Running {n_trials} bootstrap trials...")
    print(f"  Model A: {MODEL_A_CONFIG['name']}")
    print(f"  Model B: {MODEL_B_CONFIG['name']}")
    print()

    X, y = load_data()

    results_a = {"accuracy": [], "f1": [], "latency_ms": []}
    results_b = {"accuracy": [], "f1": [], "latency_ms": []}

    for seed in range(n_trials):
        acc_a, f1_a, lat_a = evaluate_model(X, y, MODEL_A_CONFIG, seed)
        acc_b, f1_b, lat_b = evaluate_model(X, y, MODEL_B_CONFIG, seed)

        results_a["accuracy"].append(acc_a)
        results_a["f1"].append(f1_a)
        results_a["latency_ms"].append(lat_a)

        results_b["accuracy"].append(acc_b)
        results_b["f1"].append(f1_b)
        results_b["latency_ms"].append(lat_b)

        if (seed + 1) % 200 == 0:
            print(f"  Completed {seed + 1}/{n_trials} trials...")

    return (
        pd.DataFrame(results_a),
        pd.DataFrame(results_b)
    )

# ─────────────────────────────────────────────────────────────────
# 5. STATISTICAL EVALUATION
# ─────────────────────────────────────────────────────────────────

def cohens_d(a, b):
    """Compute Cohen's d effect size."""
    pooled_std = np.sqrt(
        (np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2
    )
    return (np.mean(b) - np.mean(a)) / pooled_std

def run_statistical_tests(df_a, df_b):
    """Run paired t-test and compute all statistics."""
    print("=" * 60)
    print("STATISTICAL EVALUATION")
    print("=" * 60)

    metrics = ["accuracy", "f1", "latency_ms"]
    results = {}

    for metric in metrics:
        a = df_a[metric].values
        b = df_b[metric].values

        # Paired t-test (one-tailed: B > A)
        t_stat, p_two = stats.ttest_rel(b, a)
        p_one = p_two / 2 if t_stat > 0 else 1.0

        # Confidence interval for difference
        diff = b - a
        ci_low, ci_high = stats.t.interval(
            0.95,
            df=len(diff) - 1,
            loc=np.mean(diff),
            scale=stats.sem(diff)
        )

        # Effect size
        d = cohens_d(a, b)

        results[metric] = {
            "mean_a":   round(np.mean(a), 6),
            "mean_b":   round(np.mean(b), 6),
            "diff":     round(np.mean(diff), 6),
            "ci_low":   round(ci_low, 6),
            "ci_high":  round(ci_high, 6),
            "t_stat":   round(t_stat, 4),
            "p_value":  round(p_one, 6),
            "cohens_d": round(d, 4),
        }

        label = metric.upper()
        sig = "YES" if p_one < 0.05 else "NO"
        effect = (
            "large" if abs(d) > 0.8
            else "medium" if abs(d) > 0.5
            else "small" if abs(d) > 0.2
            else "negligible"
        )

        print(f"\n  [{label}]")
        print(f"    Model A mean    : {results[metric]['mean_a']:.4f}")
        print(f"    Model B mean    : {results[metric]['mean_b']:.4f}")
        print(f"    Difference (B-A): {results[metric]['diff']:+.4f}")
        print(f"    95% CI          : [{ci_low:.4f}, {ci_high:.4f}]")
        print(f"    t-statistic     : {t_stat:.4f}")
        print(f"    p-value (1-tail): {p_one:.6f}")
        print(f"    Cohen's d       : {d:.4f} ({effect})")
        print(f"    Significant?    : {sig}")

    return results

# ─────────────────────────────────────────────────────────────────
# 6. GUARDRAIL CHECK
# ─────────────────────────────────────────────────────────────────

def check_guardrails(stats_results):
    """Check if Model B passes latency guardrail."""
    print("\n" + "=" * 60)
    print("GUARDRAIL CHECK")
    print("=" * 60)

    lat_a = stats_results["latency_ms"]["mean_a"]
    lat_b = stats_results["latency_ms"]["mean_b"]
    ratio = lat_b / lat_a if lat_a > 0 else 999

    passed = ratio <= 1.5
    status = "PASSED" if passed else "FAILED"

    print(f"\n  Latency Model A : {lat_a:.2f} ms")
    print(f"  Latency Model B : {lat_b:.2f} ms")
    print(f"  Ratio (B/A)     : {ratio:.3f}x")
    print(f"  Threshold       : <= 1.5x")
    print(f"  Guardrail       : {status}")

    return passed

# ─────────────────────────────────────────────────────────────────
# 7. VISUALIZATIONS
# ─────────────────────────────────────────────────────────────────

def plot_accuracy_distributions(df_a, df_b):
    """Plot accuracy distributions for both models."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    metrics = [
        ("accuracy", "Accuracy", "steelblue", "tomato"),
        ("f1",       "F1 Score", "steelblue", "tomato"),
        ("latency_ms", "Latency (ms)", "steelblue", "tomato"),
    ]

    for ax, (col, label, ca, cb) in zip(axes, metrics):
        ax.hist(df_a[col], bins=30, alpha=0.6,
                color=ca, label="Model A (v1.0)")
        ax.hist(df_b[col], bins=30, alpha=0.6,
                color=cb, label="Model B (v1.1)")
        ax.axvline(df_a[col].mean(), color=ca,
                   linestyle="--", linewidth=2)
        ax.axvline(df_b[col].mean(), color=cb,
                   linestyle="--", linewidth=2)
        ax.set_title(f"{label} Distribution\n"
                     f"A={df_a[col].mean():.4f} | "
                     f"B={df_b[col].mean():.4f}",
                     fontsize=11, fontweight="bold")
        ax.set_xlabel(label)
        ax.set_ylabel("Trial Count")
        ax.legend()
        ax.grid(alpha=0.3)

    plt.suptitle(
        "A/B Test: Model A vs Model B - 1000 Bootstrap Trials\n"
        "IrisClassifier | IDS 568 Final Project",
        fontsize=13, fontweight="bold"
    )
    plt.tight_layout()
    plt.savefig("visualizations/ab_test_distributions.png",
                dpi=150, bbox_inches="tight")
    plt.close()
    print("\nSaved: visualizations/ab_test_distributions.png")

def plot_difference_ci(stats_results):
    """Plot mean difference with confidence intervals."""
    metrics = ["accuracy", "f1"]
    labels  = ["Accuracy", "F1 Score"]
    diffs   = [stats_results[m]["diff"]    for m in metrics]
    ci_low  = [stats_results[m]["ci_low"]  for m in metrics]
    ci_high = [stats_results[m]["ci_high"] for m in metrics]
    err_low  = [d - l for d, l in zip(diffs, ci_low)]
    err_high = [h - d for d, h in zip(diffs, ci_high)]

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["tomato" if d < 0 else "steelblue" for d in diffs]

    ax.barh(labels, diffs, xerr=[err_low, err_high],
            color=colors, alpha=0.8, capsize=6,
            error_kw={"elinewidth": 2})
    ax.axvline(0, color="black", linestyle="-", linewidth=1.5)
    ax.axvline(0.02, color="green", linestyle="--",
               linewidth=1.5, label="MDE threshold (+0.02)")

    for i, (d, label) in enumerate(zip(diffs, labels)):
        ax.text(d + 0.001, i, f"{d:+.4f}",
                va="center", fontsize=11, fontweight="bold")

    ax.set_title(
        "Mean Difference (B - A) with 95% Confidence Intervals\n"
        "IrisClassifier A/B Test",
        fontsize=12, fontweight="bold"
    )
    ax.set_xlabel("Difference (Model B - Model A)")
    ax.legend()
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig("visualizations/ab_test_ci.png",
                dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: visualizations/ab_test_ci.png")

# ─────────────────────────────────────────────────────────────────
# 8. DECISION
# ─────────────────────────────────────────────────────────────────

def make_decision(stats_results, guardrail_passed):
    """Apply decision rules and print recommendation."""
    print("\n" + "=" * 60)
    print("DECISION")
    print("=" * 60)

    acc_p     = stats_results["accuracy"]["p_value"]
    acc_d     = stats_results["accuracy"]["cohens_d"]
    acc_diff  = stats_results["accuracy"]["diff"]

    print(f"\n  Accuracy p-value  : {acc_p:.6f} (threshold: 0.05)")
    print(f"  Cohen's d         : {acc_d:.4f} (threshold: 0.2)")
    print(f"  Mean difference   : {acc_diff:+.4f} (threshold: +0.02)")
    print(f"  Guardrail passed  : {guardrail_passed}")

    if not guardrail_passed:
        decision = "KEEP MODEL A"
        reason   = "Latency guardrail failed - Model B too slow"
    elif acc_p < 0.05 and abs(acc_d) > 0.2 and acc_diff >= 0.02:
        decision = "SHIP MODEL B"
        reason   = ("Statistically significant improvement with "
                    "meaningful effect size")
    elif acc_p < 0.05 and abs(acc_d) <= 0.2:
        decision = "RUN MORE DATA"
        reason   = ("Statistically significant but effect size "
                    "too small to be practically meaningful")
    else:
        decision = "KEEP MODEL A"
        reason   = "No statistically significant improvement detected"

    print(f"\n  DECISION : {decision}")
    print(f"  REASON   : {reason}")
    print("\n" + "=" * 60)

    return decision, reason

# ─────────────────────────────────────────────────────────────────
# 9. MAIN
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("A/B TEST SIMULATION - IrisClassifier v1.0 vs v1.1")
    print("IDS 568 MLOps - Module 8 Final Project")
    print("=" * 60)
    print()

    # Run simulation
    df_a, df_b = run_simulation(n_trials=1000)

    # Statistical evaluation
    stats_results = run_statistical_tests(df_a, df_b)

    # Guardrail check
    guardrail_passed = check_guardrails(stats_results)

    # Visualizations
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    plot_accuracy_distributions(df_a, df_b)
    plot_difference_ci(stats_results)

    # Decision
    decision, reason = make_decision(stats_results, guardrail_passed)

    print("\nDone! Check visualizations/ folder for plots.")
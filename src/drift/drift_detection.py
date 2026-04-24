"""
Drift Detection Script: IrisClassifier v1.0
Component 4 - Data Integrity & Drift Detection
IDS 568 MLOps - Module 8 Final Project
Author: Parth Patel (ppatel)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.datasets import load_iris

# ── Output directory ──────────────────────────────────────────────
os.makedirs("visualizations", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ─────────────────────────────────────────────────────────────────
# 1. GENERATE REFERENCE & PRODUCTION DATASETS
# ─────────────────────────────────────────────────────────────────

def generate_reference_data(seed=42):
    """Reference dataset = original Iris training distribution."""
    iris = load_iris(as_frame=True)
    df = iris.frame.copy()
    df.columns = [
        "sepal_length", "sepal_width",
        "petal_length", "petal_width", "target"
    ]
    return df

def generate_production_data(seed=99, drift_strength=0.5):
    """
    Simulated production data with intentional drift injected:
    - petal_length: strong drift (mean shift + variance change)
    - petal_width:  moderate drift (mean shift)
    - sepal_length: slight drift
    - sepal_width:  minimal drift (stable)
    """
    np.random.seed(seed)
    iris = load_iris(as_frame=True)
    df = iris.frame.copy()
    df.columns = [
        "sepal_length", "sepal_width",
        "petal_length", "petal_width", "target"
    ]

    n = len(df)

    # Inject drift into features
    df["petal_length"] = df["petal_length"] + np.random.normal(
        drift_strength * 1.2, 0.4, n
    )
    df["petal_width"] = df["petal_width"] + np.random.normal(
        drift_strength * 0.7, 0.3, n
    )
    df["sepal_length"] = df["sepal_length"] + np.random.normal(
        drift_strength * 0.3, 0.2, n
    )
    df["sepal_width"] = df["sepal_width"] + np.random.normal(
        drift_strength * 0.1, 0.1, n
    )

    return df

# ─────────────────────────────────────────────────────────────────
# 2. PSI (POPULATION STABILITY INDEX)
# ─────────────────────────────────────────────────────────────────

def compute_psi(reference, production, bins=10):
    """
    Compute PSI between reference and production distributions.
    PSI < 0.1  : No significant drift
    PSI 0.1-0.2: Moderate drift - monitor closely
    PSI > 0.2  : Significant drift - retraining recommended
    """
    ref_min = min(reference.min(), production.min())
    ref_max = max(reference.max(), production.max())
    bin_edges = np.linspace(ref_min, ref_max, bins + 1)

    ref_counts, _ = np.histogram(reference, bins=bin_edges)
    prod_counts, _ = np.histogram(production, bins=bin_edges)

    # Add small epsilon to avoid division by zero
    ref_pct = (ref_counts + 1e-6) / len(reference)
    prod_pct = (prod_counts + 1e-6) / len(production)

    psi = np.sum((prod_pct - ref_pct) * np.log(prod_pct / ref_pct))
    return round(float(psi), 4)

def psi_severity(psi):
    if psi < 0.1:
        return "OK", "green"
    elif psi < 0.2:
        return "WARNING", "orange"
    else:
        return "CRITICAL", "red"

# ─────────────────────────────────────────────────────────────────
# 3. KS TEST
# ─────────────────────────────────────────────────────────────────

def compute_ks(reference, production):
    """
    Kolmogorov-Smirnov test for distribution shift.
    Returns statistic and p-value.
    p < 0.05 means distributions are significantly different.
    """
    stat, pvalue = stats.ks_2samp(reference, production)
    return round(float(stat), 4), round(float(pvalue), 4)

# ─────────────────────────────────────────────────────────────────
# 4. OUTLIER / INTEGRITY DETECTION
# ─────────────────────────────────────────────────────────────────

def detect_outliers(df, features):
    """
    Detect outliers using IQR method.
    Returns count and percentage of outlier rows per feature.
    """
    results = {}
    for feat in features:
        Q1 = df[feat].quantile(0.25)
        Q3 = df[feat].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outlier_mask = (df[feat] < lower) | (df[feat] > upper)
        count = outlier_mask.sum()
        pct = round(100 * count / len(df), 2)
        results[feat] = {
            "outlier_count": int(count),
            "outlier_pct": pct,
            "lower_bound": round(lower, 4),
            "upper_bound": round(upper, 4)
        }
    return results

# ─────────────────────────────────────────────────────────────────
# 5. VISUALIZATIONS
# ─────────────────────────────────────────────────────────────────

def plot_drift_distributions(ref_df, prod_df, features):
    """Plot reference vs production distributions for each feature."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for i, feat in enumerate(features):
        ax = axes[i]
        ax.hist(ref_df[feat], bins=20, alpha=0.6,
                color="steelblue", label="Reference (Training)")
        ax.hist(prod_df[feat], bins=20, alpha=0.6,
                color="tomato", label="Production (Simulated)")
        psi = compute_psi(ref_df[feat].values, prod_df[feat].values)
        severity, color = psi_severity(psi)
        ax.set_title(
            f"{feat}\nPSI={psi} [{severity}]",
            color=color, fontsize=12, fontweight="bold"
        )
        ax.set_xlabel("Value (cm)")
        ax.set_ylabel("Count")
        ax.legend()
        ax.grid(alpha=0.3)

    plt.suptitle(
        "Feature Drift: Reference vs Production Distribution\n"
        "IrisClassifier v1.0 | IDS 568 Final Project",
        fontsize=14, fontweight="bold", y=1.02
    )
    plt.tight_layout()
    plt.savefig("visualizations/drift_distributions.png",
                dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: visualizations/drift_distributions.png")

def plot_psi_summary(psi_scores):
    """Bar chart of PSI scores with threshold lines."""
    features = list(psi_scores.keys())
    values = list(psi_scores.values())
    colors = [psi_severity(v)[1] for v in values]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(features, values, color=colors, edgecolor="black",
                  alpha=0.85)

    ax.axhline(0.1, color="orange", linestyle="--",
               linewidth=1.5, label="Warning threshold (0.1)")
    ax.axhline(0.2, color="red", linestyle="--",
               linewidth=1.5, label="Critical threshold (0.2)")

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.005,
                f"{val:.3f}", ha="center", va="bottom",
                fontsize=11, fontweight="bold")

    ax.set_title(
        "PSI Drift Score by Feature\nIrisClassifier v1.0",
        fontsize=13, fontweight="bold"
    )
    ax.set_ylabel("PSI Score")
    ax.set_xlabel("Feature")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("visualizations/psi_summary.png",
                dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: visualizations/psi_summary.png")

def plot_drift_over_time(ref_df, features, windows=8):
    """
    Simulate drift growing over time windows.
    Each window adds slightly more drift to production data.
    """
    time_psi = {feat: [] for feat in features}

    for w in range(1, windows + 1):
        prod = generate_production_data(
            seed=w, drift_strength=w * 0.15
        )
        for feat in features:
            psi = compute_psi(
                ref_df[feat].values, prod[feat].values
            )
            time_psi[feat].append(psi)

    fig, ax = plt.subplots(figsize=(12, 6))
    x = list(range(1, windows + 1))

    colors_map = {
        "sepal_length": "steelblue",
        "sepal_width": "green",
        "petal_length": "tomato",
        "petal_width": "orange"
    }

    for feat in features:
        ax.plot(x, time_psi[feat], marker="o",
                label=feat, linewidth=2,
                color=colors_map.get(feat, "gray"))

    ax.axhline(0.1, color="orange", linestyle="--",
               linewidth=1.5, label="Warning (0.1)")
    ax.axhline(0.2, color="red", linestyle="--",
               linewidth=1.5, label="Critical (0.2)")

    ax.set_title(
        "PSI Drift Score Over Time Windows\nIrisClassifier v1.0",
        fontsize=13, fontweight="bold"
    )
    ax.set_xlabel("Time Window")
    ax.set_ylabel("PSI Score")
    ax.set_xticks(x)
    ax.set_xticklabels([f"W{i}" for i in x])
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("visualizations/drift_over_time.png",
                dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: visualizations/drift_over_time.png")

def plot_label_distribution(ref_df, prod_df):
    """Compare class label distributions."""
    ref_counts = ref_df["target"].value_counts().sort_index()
    prod_counts = prod_df["target"].value_counts().sort_index()

    labels = ["Setosa (0)", "Versicolor (1)", "Virginica (2)"]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width/2, ref_counts.values, width,
           label="Reference", color="steelblue", alpha=0.8)
    ax.bar(x + width/2, prod_counts.values, width,
           label="Production", color="tomato", alpha=0.8)

    ax.set_title(
        "Label Distribution: Reference vs Production\n"
        "IrisClassifier v1.0",
        fontsize=13, fontweight="bold"
    )
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Sample Count")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("visualizations/label_distribution.png",
                dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: visualizations/label_distribution.png")

# ─────────────────────────────────────────────────────────────────
# 6. MAIN REPORT
# ─────────────────────────────────────────────────────────────────

def run_drift_report():
    print("=" * 60)
    print("DRIFT DETECTION REPORT - IrisClassifier v1.0")
    print("IDS 568 MLOps - Module 8 Final Project")
    print("=" * 60)

    features = [
        "sepal_length", "sepal_width",
        "petal_length", "petal_width"
    ]

    # Generate datasets
    ref_df = generate_reference_data()
    prod_df = generate_production_data()

    print("\n[1] DATASET SUMMARY")
    print(f"    Reference samples : {len(ref_df)}")
    print(f"    Production samples: {len(prod_df)}")

    # PSI scores
    print("\n[2] PSI DRIFT SCORES")
    print(f"    {'Feature':<16} {'PSI':>6}  {'Status'}")
    print(f"    {'-'*40}")
    psi_scores = {}
    for feat in features:
        psi = compute_psi(ref_df[feat].values, prod_df[feat].values)
        severity, _ = psi_severity(psi)
        psi_scores[feat] = psi
        print(f"    {feat:<16} {psi:>6.4f}  {severity}")

    # KS test
    print("\n[3] KS TEST RESULTS")
    print(f"    {'Feature':<16} {'KS Stat':>8}  {'p-value':>8}  "
          f"{'Drift?'}")
    print(f"    {'-'*50}")
    for feat in features:
        ks_stat, pval = compute_ks(
            ref_df[feat].values, prod_df[feat].values
        )
        drift = "YES" if pval < 0.05 else "NO"
        print(f"    {feat:<16} {ks_stat:>8.4f}  {pval:>8.4f}  "
              f"{drift}")

    # Outliers
    print("\n[4] OUTLIER / INTEGRITY CHECK (Production Data)")
    outliers = detect_outliers(prod_df, features)
    print(f"    {'Feature':<16} {'Outliers':>9}  {'Pct%':>6}")
    print(f"    {'-'*36}")
    for feat, info in outliers.items():
        print(f"    {feat:<16} {info['outlier_count']:>9}  "
              f"{info['outlier_pct']:>5}%")

    # Visualizations
    print("\n[5] GENERATING VISUALIZATIONS...")
    plot_drift_distributions(ref_df, prod_df, features)
    plot_psi_summary(psi_scores)
    plot_drift_over_time(ref_df, features)
    plot_label_distribution(ref_df, prod_df)

    print("\n[6] SUMMARY & RECOMMENDATION")
    critical = [f for f, p in psi_scores.items() if p >= 0.2]
    warning  = [
        f for f, p in psi_scores.items() if 0.1 <= p < 0.2
    ]
    if critical:
        print(f"    CRITICAL drift detected in: {critical}")
        print("    ACTION: Retraining pipeline recommended NOW")
    if warning:
        print(f"    WARNING drift detected in : {warning}")
        print("    ACTION: Monitor closely, schedule retraining")
    if not critical and not warning:
        print("    All features stable. No action required.")

    print("\n" + "=" * 60)
    print("Report complete. Check visualizations/ folder.")
    print("=" * 60)

if __name__ == "__main__":
    run_drift_report()
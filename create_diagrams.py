import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

os.makedirs("docs", exist_ok=True)

# ── DIAGRAM 1: Lineage Diagram ────────────────────────────────
fig, ax = plt.subplots(1, 1, figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

boxes = [
    (5.0, 12.5, 'DATA SOURCE\nUCI Iris Dataset\n150 samples, 4 features', '#4A90D9'),
    (5.0, 10.5, 'PREPROCESSING\npreprocess.py\nNormalize, dropna, SHA256 hash', '#5BA85A'),
    (5.0, 8.5,  'TRAINING\ntrain.py\nRandomForest n=100 depth=5 seed=42', '#E8A838'),
    (5.0, 6.5,  'EXPERIMENT TRACKING\nMLflow - 5 runs logged\nparams, metrics, artifacts, hashes', '#9B59B6'),
    (5.0, 4.5,  'EVALUATION\nmodel_validation.py\naccuracy>=0.85, f1>=0.85', '#E74C3C'),
    (5.0, 2.5,  'MODEL REGISTRY\nMLflow Registry\nNone -> Staging -> Production', '#1ABC9C'),
    (5.0, 0.5,  'DEPLOYMENT + MONITORING\nFastAPI Cloud Run\nPrometheus + Grafana', '#E67E22'),
]

for x, y, text, color in boxes:
    rect = mpatches.FancyBboxPatch(
        (x-3.5, y-0.7), 7.0, 1.4,
        boxstyle='round,pad=0.1',
        facecolor=color, edgecolor='white',
        linewidth=2, alpha=0.9
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=9, color='white', fontweight='bold')

for i in range(len(boxes)-1):
    x = boxes[i][0]
    y1 = boxes[i][1]
    y2 = boxes[i+1][1]
    ax.annotate('', xy=(x, y2+0.7), xytext=(x, y1-0.7),
                arrowprops=dict(arrowstyle='->', color='white', lw=2))

ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#1a1a2e')
plt.title(
    'IrisClassifier v1.0 - Model Lineage Diagram\n'
    'IDS 568 MLOps Final Project | Parth Patel (ppatel)',
    color='white', fontsize=12, fontweight='bold', pad=15
)
plt.tight_layout()
plt.savefig('docs/lineage-diagram.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("Saved: docs/lineage-diagram.png")

# ── DIAGRAM 2: System Boundary Diagram ───────────────────────
fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

components = [
    (1.2, 4.0, 'INPUT\nFeatures\n4 float values',     '#4A90D9', 1.8, 1.4),
    (3.8, 5.5, 'VALIDATION\nPydantic Schema\nrange checks', '#E8A838', 1.8, 1.2),
    (3.8, 2.5, 'MONITORING\nPrometheus\nmetrics emit', '#9B59B6', 1.8, 1.2),
    (6.5, 4.0, 'ML MODEL\nRandomForest\nv1.0 inference', '#E74C3C', 2.0, 1.4),
    (9.5, 5.5, 'MLflow\nRegistry\nversion control',    '#1ABC9C', 1.8, 1.2),
    (9.5, 2.5, 'Grafana\nDashboard\nalerts',           '#E67E22', 1.8, 1.2),
    (12.5, 4.0,'OUTPUT\nPrediction\nclass+confidence', '#5BA85A', 1.8, 1.4),
]

for x, y, text, color, w, h in components:
    rect = mpatches.FancyBboxPatch(
        (x-w/2, y-h/2), w, h,
        boxstyle='round,pad=0.1',
        facecolor=color, edgecolor='white',
        linewidth=2, alpha=0.9
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=8.5, color='white', fontweight='bold')

arrows = [
    (2.1, 4.0, 2.9, 4.7),
    (2.1, 4.0, 2.9, 3.3),
    (4.7, 5.5, 5.5, 4.5),
    (4.7, 2.5, 5.5, 3.5),
    (7.5, 4.0, 8.6, 4.7),
    (7.5, 4.0, 8.6, 3.3),
    (10.4, 5.5, 11.6, 4.5),
    (10.4, 2.5, 11.6, 3.5),
]

for x1, y1, x2, y2 in arrows:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

boundary = mpatches.FancyBboxPatch(
    (0.2, 0.5), 13.6, 7.0,
    boxstyle='round,pad=0.1',
    facecolor='none', edgecolor='#4A90D9',
    linewidth=2, linestyle='--', alpha=0.5
)
ax.add_patch(boundary)
ax.text(7.0, 7.7,
        'SYSTEM BOUNDARY: IrisClassifier v1.0',
        ha='center', color='#4A90D9',
        fontsize=10, fontweight='bold')

ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#1a1a2e')
plt.title(
    'System Boundary Diagram - IrisClassifier v1.0\n'
    'IDS 568 MLOps Final Project | Parth Patel (ppatel)',
    color='white', fontsize=11, fontweight='bold'
)
plt.tight_layout()
plt.savefig('docs/system-boundary-diagram.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print("Saved: docs/system-boundary-diagram.png")

print("\nBoth diagrams created successfully!")
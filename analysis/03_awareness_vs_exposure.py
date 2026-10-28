#!/usr/bin/env python3
"""A3 Awareness versus exposure: predicted findability against measured address exposure; the prediction gap by tenure."""
import sys, os
import numpy as np, pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from common import load, save, label, BANDS, BAND_COLORS


def run(which="synthetic"):
    P = load(which)["participants"]
    lines = ["## A3 Awareness versus exposure", ""]
    for x, y, name in [("predicted_findability", "address_sites", "A11 predicted findability × address sites (score 2)"),
                       ("predicted_relatives", "relatives_sites", "A12 predicted relatives × relatives sites (score 2)"),
                       ("awareness_index", "exposure_score", "awareness index × exposure score")]:
        if x in P and y in P:
            r, p = stats.spearmanr(P[x], P[y])
            lines.append(f"- Spearman rho, {name}: {r:.2f} (p = {p:.3f})")
    z = lambda s: (s - s.mean()) / s.std()
    P["prediction_gap"] = z(P.address_sites) - z(P.predicted_findability)
    gap = P.groupby("tenure_band").prediction_gap.agg(n="count", median="median", mean="mean").reindex(BANDS).round(2)
    H, p = stats.kruskal(*[P.loc[P.tenure_band == b, "prediction_gap"] for b in BANDS])
    lines += ["", "Prediction gap (standardised address exposure minus standardised predicted findability; positive = more exposed than expected):", "",
              gap.to_markdown(), "", f"Kruskal–Wallis across tenure bands: H = {H:.2f}, p = {p:.4f}", ""]
    tab = pd.crosstab(P.predicted_findability, P.address_sites)
    lines += ["Predicted findability (rows, 1 very unlikely … 4 very likely) × number of sites with accurate address (columns):", "", tab.to_markdown(), ""]

    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    rng = np.random.default_rng(3)
    for b in BANDS:
        sub = P[P.tenure_band == b]
        ax.scatter(sub.predicted_findability + rng.normal(0, 0.08, len(sub)), sub.address_sites + rng.normal(0, 0.08, len(sub)),
                   s=28, alpha=0.75, color=BAND_COLORS[b], label=b, edgecolor="white", lw=0.5)
    ax.plot([1, 4], [0, 6], ls="--", color="grey", lw=1, label="expectation matches exposure")
    ax.set_xticks([1, 2, 3, 4]); ax.set_xticklabels(["very\nunlikely", "unlikely", "likely", "very\nlikely"])
    ax.set_xlabel("Predicted findability of own address (asked before any lookup)")
    ax.set_ylabel("Sites showing an accurate current address (0–6)")
    ax.set_title(f"Expectation versus measured exposure ({label(which)})")
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    save(fig, "03_awareness_vs_exposure.png", which)
    return "\n".join(lines)


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "synthetic"))

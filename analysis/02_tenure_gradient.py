#!/usr/bin/env python3
"""A2 Tenure gradient: Kruskal–Wallis across tenure bands, pairwise Mann–Whitney (Holm), Cliff's delta, OLS with HC3."""
import sys, os, itertools
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from common import load, save, label, BANDS, BAND_COLORS


def cliffs_delta(a, b):
    a, b = np.asarray(a), np.asarray(b)
    more = sum((x > b).sum() for x in a); less = sum((x < b).sum() for x in a)
    return (more - less) / (len(a) * len(b))


def holm(pvals):
    order = np.argsort(pvals); m = len(pvals); adj = np.empty(m)
    running = 0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * pvals[idx]); adj[idx] = min(1, running)
    return adj


def run(which="synthetic"):
    P = load(which)["participants"]
    groups = [P.loc[P.tenure_band == b, "exposure_score"].values for b in BANDS]
    H, p = stats.kruskal(*groups)
    lines = ["## A2 Tenure gradient", "", "Exposure score by tenure band:", "",
             P.groupby("tenure_band").exposure_score.agg(n="count", median="median", mean="mean", sd="std").reindex(BANDS).round(1).to_markdown(), "",
             f"Kruskal–Wallis H = {H:.2f}, p = {p:.4f}", ""]
    pairs = list(itertools.combinations(range(3), 2)); ps = []; deltas = []
    rng = np.random.default_rng(2026)
    for i, j in pairs:
        u, pp = stats.mannwhitneyu(groups[i], groups[j], alternative="two-sided"); ps.append(pp)
        dl = cliffs_delta(groups[j], groups[i])
        boots = [cliffs_delta(rng.choice(groups[j], len(groups[j])), rng.choice(groups[i], len(groups[i]))) for _ in range(1000)]
        deltas.append((dl, np.percentile(boots, 2.5), np.percentile(boots, 97.5)))
    adj = holm(np.array(ps))
    lines += ["Pairwise (later band minus earlier band):", "", "| comparison | Mann–Whitney p (Holm) | Cliff's delta [95% CI] |", "|---|---|---|"]
    for (i, j), pa, (dl, lo, hi) in zip(pairs, adj, deltas):
        lines.append(f"| {BANDS[j]} vs {BANDS[i]} | {pa:.4f} | {dl:.2f} [{lo:.2f}, {hi:.2f}] |")
    # OLS
    tenure_col = "tenure_years" if "tenure_years" in P else None
    formula = ("exposure_score ~ tenure_years + C(occupation_band) + household_size + own_record" if tenure_col
               else "exposure_score ~ C(tenure_band) + C(occupation_band) + household_size + own_record")
    m = smf.ols(formula, data=P).fit(cov_type="HC3")
    ci = m.conf_int()
    tab = pd.DataFrame({"coef": m.params, "2.5%": ci[0], "97.5%": ci[1], "p": m.pvalues}).round(3)
    lines += ["", f"OLS (HC3): {formula}", "", tab.to_markdown(), "", f"R² = {m.rsquared:.3f}, n = {int(m.nobs)}", ""]

    fig, ax = plt.subplots(figsize=(6, 3.6))
    bp = ax.boxplot(groups, patch_artist=True, widths=0.5, showfliers=False); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(BANDS)
    for patch, b in zip(bp["boxes"], BANDS): patch.set_facecolor(BAND_COLORS[b]); patch.set_alpha(0.6)
    for k, g in enumerate(groups):
        ax.scatter(np.random.default_rng(k).normal(k + 1, 0.06, len(g)), g, s=12, color="black", alpha=0.5, zorder=3)
    ax.set_ylabel("Exposure score (0–84)"); ax.set_ylim(0, 84)
    ax.set_title(f"Exposure by tenure in the U.S. (Kruskal–Wallis p = {p:.3f}) ({label(which)})")
    save(fig, "02_tenure_gradient.png", which)
    return "\n".join(lines)


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "synthetic"))

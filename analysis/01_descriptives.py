#!/usr/bin/env python3
"""A1 Descriptives: exposure distribution, per-site and per-field prevalence, heatmap ordered by tenure."""
import sys, os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from common import load, save, label, SITES, FIELDS, BANDS, BAND_COLORS


def run(which="synthetic"):
    d = load(which)
    P, G = d["participants"], d["exposure_grid"]
    lines = ["## A1 Descriptives", "", f"n = {len(P)}", "",
             f"Exposure score: median {P.exposure_score.median():.0f}, IQR {P.exposure_score.quantile(.25):.0f}–{P.exposure_score.quantile(.75):.0f}, "
             f"mean {P.exposure_score.mean():.1f} (SD {P.exposure_score.std():.1f}), range {P.exposure_score.min()}–{P.exposure_score.max()}", ""]

    # histogram
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.hist(P.exposure_score, bins=range(0, 86, 6), color="#4C72B0", edgecolor="white")
    ax.set_xlabel("Exposure score (0–84)"); ax.set_ylabel("Participants")
    ax.set_title(f"Distribution of exposure scores ({label(which)})")
    save(fig, "01a_exposure_histogram.png", which)

    if G is not None:
        # per-site, per-field prevalence of score 2
        prev = G.assign(two=(G.score == 2).astype(int)).pivot_table(index="field", columns="site", values="two", aggfunc="mean")
        prev = prev.reindex(index=FIELDS, columns=SITES)
        lines += ["Share of cells scoring 2 (accurate and current), by field and site:", "", prev.round(2).to_markdown(), ""]
        site_mean = G.groupby("site").score.mean().reindex(SITES)
        lines += ["Mean cell score by site:", "", site_mean.round(2).to_frame("mean score").to_markdown(), ""]

        # heatmap: participants (rows, ordered by tenure) x site-field (cols)
        order = P.sort_values("tenure_years" if "tenure_years" in P else "tenure_band").id.tolist()
        G["col"] = G.site.str.replace("TruePeopleSearch", "TPS").str.replace("FastPeopleSearch", "FPS") + "\n" + G.field.str.replace("Court/public records", "Records").str.replace("Current address", "Address").str.replace("Past addresses", "Past addr")
        cols = [f"{s.replace('TruePeopleSearch','TPS').replace('FastPeopleSearch','FPS')}\n{f.replace('Court/public records','Records').replace('Current address','Address').replace('Past addresses','Past addr')}" for s in SITES for f in FIELDS]
        M = G.pivot_table(index="id", columns="col", values="score").reindex(index=order, columns=cols)
        fig, ax = plt.subplots(figsize=(13, max(4, 0.16 * len(order) + 1)))
        im = ax.imshow(M.values, aspect="auto", cmap="Blues", vmin=0, vmax=2)
        ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=90, fontsize=6)
        ax.set_yticks(range(len(order))); ax.set_yticklabels(order, fontsize=5)
        for i in range(1, len(SITES)):
            ax.axvline(i * len(FIELDS) - 0.5, color="white", lw=2)
        band_of = P.set_index("id").tenure_band
        for y, pid in enumerate(order):
            ax.add_patch(plt.Rectangle((-1.5, y - 0.5), 0.8, 1, color=BAND_COLORS[band_of[pid]], clip_on=False))
        ax.set_xlim(-1.6, len(cols) - 0.5)
        cb = fig.colorbar(im, ax=ax, ticks=[0, 1, 2], fraction=0.02); cb.ax.set_yticklabels(["0 not shown", "1 partial", "2 accurate"])
        ax.set_title(f"Exposure grid, participants ordered by tenure (colour bar at left: tenure band) ({label(which)})")
        handles = [plt.Rectangle((0, 0), 1, 1, color=BAND_COLORS[b]) for b in BANDS]
        ax.legend(handles, BANDS, loc="upper left", bbox_to_anchor=(1.08, 1), fontsize=7, frameon=False)
        save(fig, "01b_exposure_heatmap.png", which)
    return "\n".join(lines)


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "synthetic"))

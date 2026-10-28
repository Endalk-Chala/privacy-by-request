#!/usr/bin/env python3
"""A6.2 Institution data-flow graph from the settlement timeline.

Directed graph: institution (event type) -> named recipient type, plus an "unknown" sink for events where the
participant named no downstream holder. Edge weight = participants naming that flow. Node attribute =
known-recipient ratio per institution. Only aggregates are drawn; no participant-level data appear.
"""
import sys, os
import numpy as np, pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from common import load, save, label


def run(which="synthetic"):
    T = load(which)["timeline"]
    if T is None:
        return "## A6.2 Institution data-flow graph\n\ntimeline.csv not available in this tier; skipped."
    T = T.copy()
    T["recipient"] = np.where(T.named_downstream_holder.eq("Yes"), T.named_recipient_type.fillna("other"), "unknown")
    inst = T.groupby("event_type").agg(events=("id", "size"), participants=("id", "nunique"),
                                       known=("named_downstream_holder", lambda s: (s == "Yes").mean())).sort_values("participants", ascending=False)
    flows = T.groupby(["event_type", "recipient"]).id.nunique().reset_index(name="participants")
    lines = ["## A6.2 Institution data-flow graph", "", "Institutions ranked by participants mentioning them, with the share of their events for which any downstream holder was named:", "",
             inst.rename(columns={"known": "known-recipient ratio"}).round(2).to_markdown(), "",
             f"Overall known-recipient ratio: {(T.named_downstream_holder == 'Yes').mean():.2f} across {len(T)} events from {T.id.nunique()} participants.", ""]

    G = nx.DiGraph()
    for _, r in flows.iterrows():
        G.add_edge(r.event_type, r.recipient, weight=int(r.participants))
    insts = list(inst.index); recips = [n for n in G.nodes if n not in insts]
    recips = sorted(recips, key=lambda n: (n == "unknown", n))
    pos = {n: (0, -i) for i, n in enumerate(insts)}
    pos.update({n: (3, -i * (len(insts) - 1) / max(1, len(recips) - 1)) for i, n in enumerate(recips)})
    fig, ax = plt.subplots(figsize=(9, 0.42 * len(insts) + 1.5))
    w = np.array([d["weight"] for _, _, d in G.edges(data=True)])
    for (u, v, d) in G.edges(data=True):
        ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="-", lw=0.3 + 4 * d["weight"] / w.max(),
                    color="#C44E52" if v == "unknown" else "#4C72B0", alpha=0.45, shrinkA=8, shrinkB=8))
    cmap = plt.get_cmap("Blues")
    for n in insts:
        ax.scatter(*pos[n], s=60 + 12 * inst.loc[n, "participants"], color=cmap(0.3 + 0.7 * inst.loc[n, "known"]), edgecolor="black", lw=0.5, zorder=3)
        ax.text(pos[n][0] - 0.12, pos[n][1], f"{n}  ({inst.loc[n, 'known']:.0%} named)", ha="right", va="center", fontsize=7)
    for n in recips:
        ax.scatter(*pos[n], s=200, color="#C44E52" if n == "unknown" else "#55A868", edgecolor="black", lw=0.5, zorder=3)
        ax.text(pos[n][0] + 0.12, pos[n][1], n, ha="left", va="center", fontsize=8)
    ax.set_xlim(-2.6, 4.6); ax.set_axis_off()
    ax.set_title(f"Where settlement-era data went, as participants could name it\n(left: institutions, shaded by share of events with a named downstream holder; right: named recipients; red = no holder named) ({label(which)})", fontsize=8)
    save(fig, "05_dataflow_network.png", which)
    return "\n".join(lines)


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "synthetic"))

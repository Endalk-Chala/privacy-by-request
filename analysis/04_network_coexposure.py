#!/usr/bin/env python3
"""A6.1 Site-field co-exposure network.

Two-mode network (participants x 42 site-field nodes, edge where score == 2), projected onto the site-field nodes
(edge weight = number of participants with score 2 on both). Louvain communities identify exposure bundles.
No participant node appears in any output; only the projection is drawn.
"""
import sys, os, itertools
import numpy as np, pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from common import load, save, label, SITES, FIELDS

SHORT = {"TruePeopleSearch": "TPS", "FastPeopleSearch": "FPS", "BeenVerified": "BV", "Court/public records": "records",
         "Current address": "address", "Past addresses": "past addr"}
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]


def run(which="synthetic", threshold=2):
    G = load(which)["exposure_grid"]
    if G is None:
        return "## A6.1 Co-exposure network\n\nexposure_grid.csv not available in this tier; skipped."
    hit = G[G.score >= threshold].copy()
    hit["node"] = hit.site.map(lambda s: SHORT.get(s, s)) + ":" + hit.field.map(lambda f: SHORT.get(f, f).lower())
    nodes = sorted(hit.node.unique())
    B = nx.Graph(); B.add_nodes_from(hit.id.unique(), bipartite=0); B.add_nodes_from(nodes, bipartite=1)
    B.add_edges_from(zip(hit.id, hit.node))
    Pj = nx.bipartite.weighted_projected_graph(B, nodes)
    n_part = hit.id.nunique()
    # drop weak ties (fewer than 10% of participants co-exposed) for readability
    minw = max(2, int(0.1 * n_part))
    H = nx.Graph(((u, v, d) for u, v, d in Pj.edges(data=True) if d["weight"] >= minw))
    H.add_nodes_from(Pj.nodes)
    comms = nx.community.louvain_communities(H, weight="weight", seed=2026, resolution=1.0)
    comms = sorted(comms, key=len, reverse=True)
    mod = nx.community.modularity(H, comms, weight="weight")
    lines = ["## A6.1 Site-field co-exposure network", "",
             f"Nodes: {H.number_of_nodes()} site-field combinations with at least one participant scoring {threshold}; "
             f"edges kept where at least {minw} participants ({minw / n_part:.0%}) are co-exposed; {H.number_of_edges()} edges.",
             f"Louvain communities: {len(comms)}, modularity {mod:.3f}.", ""]
    for k, c in enumerate(comms):
        lines.append(f"- Community {k + 1} ({len(c)} nodes): " + ", ".join(sorted(c)))
    deg = sorted(nx.degree_centrality(H).items(), key=lambda kv: -kv[1])[:8]
    lines += ["", "Highest degree centrality: " + ", ".join(f"{n} ({v:.2f})" for n, v in deg), ""]

    fig, ax = plt.subplots(figsize=(11, 9))
    # community-grouped layout: communities on a ring, members clustered around their community centre
    import math
    pos = {}
    for k, c in enumerate(comms):
        cx, cy = 3.2 * math.cos(2 * math.pi * k / len(comms)), 3.2 * math.sin(2 * math.pi * k / len(comms))
        sub = H.subgraph(c)
        local = nx.spring_layout(sub, weight="weight", seed=2026, k=1.6, scale=1.0 + 0.12 * len(c))
        pos.update({n: (cx + x, cy + y) for n, (x, y) in local.items()})
    colour = {n: PALETTE[k % len(PALETTE)] for k, c in enumerate(comms) for n in c}
    w = np.array([d["weight"] for _, _, d in H.edges(data=True)])
    nx.draw_networkx_edges(H, pos, ax=ax, width=0.3 + 3 * (w / w.max() if len(w) else 1), alpha=0.35, edge_color="grey")
    sizes = [120 + 900 * nx.degree_centrality(H)[n] for n in H.nodes]
    nx.draw_networkx_nodes(H, pos, ax=ax, node_size=sizes, node_color=[colour[n] for n in H.nodes], alpha=0.9, linewidths=0.5, edgecolors="white")
    nx.draw_networkx_labels(H, pos, ax=ax, font_size=6.5, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7))
    ax.set_axis_off()
    ax.set_title(f"Co-exposure of site–field combinations (node colour = community; edge width = participants co-exposed) ({label(which)})", fontsize=9)
    save(fig, "04_coexposure_network.png", which)
    return "\n".join(lines)


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "synthetic"))

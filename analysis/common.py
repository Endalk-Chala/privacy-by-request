"""Shared loading, paths and plotting defaults for the analysis scripts."""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITES = ["Spokeo", "Whitepages", "TruePeopleSearch", "FastPeopleSearch", "BeenVerified", "Intelius"]
FIELDS = ["Current address", "Past addresses", "Phone", "Email", "Relatives", "Associates", "Court/public records"]
BANDS = ["Under 3 years", "3 to 10 years", "Over 10 years"]
BAND_COLORS = {"Under 3 years": "#4C72B0", "3 to 10 years": "#DD8452", "Over 10 years": "#55A868"}

plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 200, "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titleweight": "bold"})


def data_dir(which):
    d = os.path.join(ROOT, "data", which)
    if not os.path.isdir(d):
        raise SystemExit(f"no data directory {d}; run analysis/make_synthetic.py or place the restricted files there")
    return d


def fig_dir():
    d = os.path.join(ROOT, "figures")
    os.makedirs(d, exist_ok=True)
    return d


def load(which):
    d = data_dir(which)
    out = {"participants": pd.read_csv(os.path.join(d, "participants.csv"))}
    for name in ("exposure_grid", "timeline", "awareness"):
        p = os.path.join(d, f"{name}.csv")
        out[name] = pd.read_csv(p) if os.path.exists(p) else None
    return out


def label(which):
    return "synthetic data" if which == "synthetic" else "study data"


def save(fig, name, which):
    path = os.path.join(fig_dir(), name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {os.path.relpath(path, ROOT)}")
    return path

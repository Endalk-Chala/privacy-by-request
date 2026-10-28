#!/usr/bin/env python3
"""Runs the full pipeline and writes figures/*.png and figures/tables.md.

  python analysis/run_all.py --data synthetic     # default; uses data/synthetic/
  python analysis/run_all.py --data restricted    # PI only; uses data/restricted/
"""
import argparse, importlib.util, os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
from common import fig_dir, ROOT

SCRIPTS = ["01_descriptives", "02_tenure_gradient", "03_awareness_vs_exposure", "04_network_coexposure", "05_network_dataflow"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="synthetic", choices=["synthetic", "restricted"])
    a = ap.parse_args()
    out = [f"# Analysis output ({a.data} data), generated {dt.datetime.now():%Y-%m-%d %H:%M}", ""]
    if a.data == "synthetic":
        out += ["**These tables are computed from synthetic data and contain no findings.**", ""]
    for name in SCRIPTS:
        print(name)
        spec = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(__file__), name + ".py"))
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        out.append(mod.run(a.data)); out.append("")
    path = os.path.join(fig_dir(), "tables.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"wrote {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()

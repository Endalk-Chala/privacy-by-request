#!/usr/bin/env python3
"""
make_synthetic.py -- generates a schema-identical synthetic dataset for the Privacy by Request study.

Nothing here is derived from real participants. Values are drawn from the design assumptions in
analysis/ANALYSIS_PLAN.md (a tenure gradient in exposure, a weak link between predicted and measured
findability, and a household bundle in co-exposure) so that every analysis script can be exercised.

Outputs (data/synthetic/):
  participants.csv     one row per participant; restricted-tier schema (tenure_band, not years, plus
                       a synthetic tenure_years column kept here only because it is synthetic)
  exposure_grid.csv    participant x site x field scores (never released for real data)
  timeline.csv         settlement timeline events (never released for real data)
  awareness.csv        A1..A16 items

Usage: python analysis/make_synthetic.py [--n 50] [--seed 2026]
"""
import argparse, csv, os, random

SITES = ["Spokeo", "Whitepages", "TruePeopleSearch", "FastPeopleSearch", "BeenVerified", "Intelius"]
FIELDS = ["Current address", "Past addresses", "Phone", "Email", "Relatives", "Associates", "Court/public records"]
PAYWALLED = {"BeenVerified", "Intelius"}
OCC = ["Care & service", "Warehouse & food", "Small business", "Professional", "Other"]
REGION = ["East Africa", "Latin America", "Southeast Asia", "Other"]
EDU = ["Primary or less", "Secondary", "Post-secondary", "Graduate"]
EVENTS = ["Lease / housing", "Utility account", "Phone plan", "Bank account", "Driver's license", "Job / payroll",
          "Remittance", "Clinic / hospital", "School enrollment", "Religious community", "Government office",
          "Car purchase / insurance", "Job-site resume", "Immigration attorney", "Resettlement agency", "Other"]
RECIP = ["government", "credit bureau", "data broker or website", "employer", "landlord", "other"]
# how often each institution is connected to a named downstream holder (design assumption, not data)
KNOWN_P = {"Lease / housing": .25, "Utility account": .15, "Phone plan": .2, "Bank account": .45, "Driver's license": .35,
           "Job / payroll": .4, "Remittance": .2, "Clinic / hospital": .3, "School enrollment": .2, "Religious community": .1,
           "Government office": .5, "Car purchase / insurance": .4, "Job-site resume": .3, "Immigration attorney": .55,
           "Resettlement agency": .35, "Other": .2}


def band(t):
    return "Under 3 years" if t < 3 else ("3 to 10 years" if t <= 10 else "Over 10 years")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "data", "synthetic"))
    a = ap.parse_args()
    rng = random.Random(a.seed)
    os.makedirs(a.out, exist_ok=True)

    parts, grid, timeline, aware = [], [], [], []
    for i in range(1, a.n + 1):
        pid = f"S{i:02d}"                       # S prefix: synthetic, never confusable with real P IDs
        tenure = round(rng.choice([rng.uniform(0.5, 2.9), rng.uniform(3, 10), rng.uniform(10.1, 30)]), 1)
        occ = rng.choice(OCC)
        hh = rng.randint(1, 7)
        own_record = 1 if rng.random() < (0.35 if tenure < 3 else 0.8) else 0
        hours = round(min(16, max(0, rng.gauss(4.5, 2))), 1)
        resume_public = 1 if rng.random() < 0.45 else 0
        # latent exposure propensity: rises with tenure, own records, resume; household size adds relatives
        base = 0.15 + 0.03 * min(tenure, 15) + 0.15 * own_record + 0.1 * resume_public + 0.01 * hours
        # awareness: weakly higher with tenure and education
        edu = rng.choice(EDU)
        a1 = 1 if rng.random() < 0.3 + 0.02 * tenure else 0
        a2 = 1 if rng.random() < 0.45 + 0.02 * tenure else 0
        a3 = 1 if rng.random() < 0.15 + 0.015 * tenure else 0
        a4 = 1 if rng.random() < 0.1 else 0
        a5 = rng.choices(["Posted it", "A company sold it", "Government or public records", "Don't know"], [.25, .25, .2, .3])[0]
        a6 = 1 if a5 in ("A company sold it", "Government or public records") else 0
        awareness = a1 + a2 + a3 + a6
        pred_addr = rng.choices([1, 2, 3, 4], [.3, .3, .25, .15])[0]      # mostly "unlikely": the prediction gap
        pred_rel = rng.choices([1, 2, 3, 4], [.35, .3, .2, .15])[0]
        a13 = rng.choices(["Only that employer", "Stays on the site", "Not sure"], [.4, .3, .3])[0]
        aware.append([pid, a1, a2, a3, a4, a5, a6, rng.randint(0, 1), 0 if rng.random() < .85 else 1, 0 if rng.random() < .95 else 1,
                      rng.randint(0, 1), pred_addr, pred_rel, a13, rng.randint(0, 1), rng.randint(0, 1),
                      rng.choice(["Unsolicited recruiter call", "Relative or friend found it", "Saw it in a search", "Told by an organization", "Never learned", "Other"]),
                      awareness])

        # exposure grid with a household bundle: address, past, relatives, associates move together
        hh_bundle = rng.random() < min(0.95, base + 0.05 * hh)
        contact_bundle = rng.random() < base
        for s in SITES:
            if s in PAYWALLED:
                teaser = 1 if rng.random() < base + 0.2 else 0
                for f in FIELDS:
                    grid.append([pid, s, f, teaser])
                continue
            site_hit = rng.random() < 0.85 if s != "Whitepages" else rng.random() < 0.6
            for f in FIELDS:
                if not site_hit:
                    sc = 0
                elif f in ("Current address", "Relatives", "Associates", "Past addresses"):
                    sc = 2 if hh_bundle and rng.random() < 0.85 else (1 if rng.random() < 0.3 else 0)
                    if f == "Past addresses" and sc == 2 and tenure < 3:
                        sc = 1
                elif f in ("Phone", "Email"):
                    sc = 2 if contact_bundle and rng.random() < 0.7 else (1 if rng.random() < 0.25 else 0)
                else:
                    sc = 2 if rng.random() < 0.15 else (1 if rng.random() < 0.2 else 0)
                grid.append([pid, s, f, sc])
        rows_p = [g for g in grid if g[0] == pid]
        exposure = sum(g[3] for g in rows_p)
        address_sites = sum(1 for g in rows_p if g[2] == "Current address" and g[3] == 2)
        relatives_sites = sum(1 for g in rows_p if g[2] == "Relatives" and g[3] == 2)

        # timeline
        n_ev = rng.randint(4, 11)
        known = 0
        for e in range(1, n_ev + 1):
            et = rng.choice(EVENTS)
            named = rng.random() < KNOWN_P[et]
            known += named
            timeline.append([pid, e, rng.randint(0, 24), et, 1, 1 if rng.random() < .9 else 0, 1 if rng.random() < .7 else 0,
                             1 if rng.random() < .4 else 0, "Yes" if named else "No", rng.choice(RECIP) if named else "", rng.randint(1, 3),
                             rng.choice(["none", "relative", "caseworker", "resettlement agency", "employer", "attorney"])])
        position = ("Settled and informed" if awareness >= 3 else "Settled and unknowing") if tenure >= 3 else \
                   ("Recent and on the record" if own_record else "Recent and off the record")
        parts.append([pid, tenure, band(tenure), occ, rng.choice(REGION), edu, rng.choice(["Band 1", "Band 2", "Band 3", "Band 4", "Declined"]),
                      hh, own_record, exposure, address_sites, relatives_sites, awareness, pred_addr, pred_rel, n_ev, known,
                      round(known / n_ev, 2), hours, resume_public, position])

    def w(name, header, rows):
        with open(os.path.join(a.out, name), "w", newline="", encoding="utf-8") as fh:
            cw = csv.writer(fh); cw.writerow(header); cw.writerows(rows)
    w("participants.csv", ["id", "tenure_years", "tenure_band", "occupation_band", "region", "education_band", "income_band",
                           "household_size", "own_record", "exposure_score", "address_sites", "relatives_sites", "awareness_index",
                           "predicted_findability", "predicted_relatives", "timeline_events", "known_recipients",
                           "known_recipient_ratio", "hours_per_day", "resume_public", "position"], parts)
    w("exposure_grid.csv", ["id", "site", "field", "score"], grid)
    w("timeline.csv", ["id", "event_no", "month_after_arrival", "event_type", "gave_name", "gave_address", "gave_dob",
                       "gave_ssn_itin", "named_downstream_holder", "named_recipient_type", "confidence", "intermediary_type"], timeline)
    w("awareness.csv", ["id", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15", "A16", "awareness_index"], aware)
    print(f"synthetic data for {a.n} participants written to {os.path.abspath(a.out)}")


if __name__ == "__main__":
    main()

# Pre-specified analysis plan

Version 0.2, October 2026, written before any analysis of real data. Deviations will be logged in this file with dates.

## Data

Input: the de-identified participant file (`data/restricted/participants.csv`) plus the per-site, per-field grid (`exposure_grid.csv`, never released) and the timeline aggregates. The synthetic files in `data/synthetic/` have identical schemas and are used to develop and test every script.

## Variables

- Outcome: `exposure_score` (0 to 84); sub-scores `address_sites`, `relatives_sites` (0 to 6); per-field prevalence (share of cells scoring 2).
- Exposure predictors: `tenure_years` (continuous, restricted tier uses `tenure_band`), `occupation_band`, `household_size`, `own_record`, `timeline_events`, `hours_per_day`, `resume_public`.
- Awareness: `awareness_index` (0 to 4), `predicted_findability` (A11, 1 to 4), A12.
- Position: four categories (see codebook).

## A1. Descriptives (RQ1)

- Exposure score: n, median, IQR, mean, SD, range; histogram.
- Per site: mean score, share of participants with any 2.
- Per field: share of cells scoring 2, overall and by site (heatmap, participants ordered by tenure).

## A2. Tenure gradient (RQ1)

- H1: exposure score increases with tenure.
- Kruskal–Wallis across the three tenure bands; pairwise Mann–Whitney with Holm correction; Cliff's delta with 95% bootstrap CI for each pair.
- OLS: exposure_score ~ tenure_years + occupation_band + household_size + own_record. Report coefficients with 95% CI and R². Robust (HC3) standard errors. Residual diagnostics reported in the supplement.
- Sensitivity: the same model on `address_sites` and `relatives_sites`.
- Power note: with n = 50 and three groups, the design detects a large effect (f ≈ 0.45) at 80% power; smaller effects are reported as estimates with CIs and not as tests.

## A3. Awareness versus exposure (RQ2)

- H2: predicted findability of address (A11) is uncorrelated or weakly correlated with measured address exposure (`address_sites`); the prediction gap is larger among recent arrivals.
- Spearman correlation A11 × address_sites; A12 × relatives_sites; awareness_index × exposure_score.
- Prediction gap = standardised address_sites minus standardised A11; compared across tenure bands (Kruskal–Wallis).
- Scatter of A11 against address_sites with jitter, coloured by tenure band, identity line.

## A4. Channel contributions (RQ3, RQ4)

- OLS: exposure_score ~ timeline_events + hours_per_day + resume_public + tenure_years. Standardised coefficients with CIs.
- known_recipient_ratio: distribution; by tenure band; by institution (aggregate).
- Share of participants with `believed_one_job_only` = 1 among those with `posted_resume_online` = 1; cross-tab with `resume_public`.

## A5. Positions

- Cross-tab of the four positions with median exposure score; by occupation band.

## A6. Network analyses

### A6.1 Site-field co-exposure network

- Two-mode network: participants × 42 site-field nodes; edge weight = score (0 dropped).
- One-mode projection onto site-field nodes: edge weight = number of participants with score 2 on both nodes.
- Louvain community detection (resolution 1.0, seed fixed); report modularity and the membership of each community. Expected: a household bundle (addresses, relatives, associates) and a contact bundle (phone, email).
- Node size = degree centrality; figure saved as `figures/04_coexposure_network.png`.
- Robustness: repeat with edges restricted to score 2 only and to score ≥ 1.

### A6.2 Institution data-flow graph

- Directed graph from the settlement timeline: institution nodes (16 event types) → recipient-type nodes (government, credit bureau, data broker or website, employer, landlord, other), with an "unknown" sink for events where no downstream holder was named.
- Edge weight = number of participants naming that flow; node attribute = share of mentions with any named recipient (known-recipient ratio per institution).
- Figure `figures/05_dataflow_network.png`; table of institutions ranked by mention count and known-recipient ratio.
- Only aggregates are used; no participant-level timeline data leaves the never-released tier.

## A7. Reliability

- Exposure audit: 20% of sessions re-scored from session notes by a second coder blind to the first scores; quadratic-weighted kappa per field.
- Interview codes: 25% double-coded; percent agreement and Cohen's kappa per code.

## A8. Qualitative integration

Joint display: for each position, the median exposure score, the modal imagined searcher, the modal unit of harm, and one approved quotation.

## Software

Python 3.11+, pandas, numpy, scipy, statsmodels, networkx, matplotlib. Versions pinned in `requirements.txt`. `analysis/run_all.py` regenerates every figure and table from the input files.

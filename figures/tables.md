# Analysis output (synthetic data), generated 2026-10-27 23:29

**These tables are computed from synthetic data and contain no findings.**

## A1 Descriptives

n = 50

Exposure score: median 34, IQR 22–42, mean 33.5 (SD 12.7), range 10–61

Share of cells scoring 2 (accurate and current), by field and site:

| field                |   Spokeo |   Whitepages |   TruePeopleSearch |   FastPeopleSearch |   BeenVerified |   Intelius |
|:---------------------|---------:|-------------:|-------------------:|-------------------:|---------------:|-----------:|
| Current address      |     0.44 |         0.34 |               0.54 |               0.52 |              0 |          0 |
| Past addresses       |     0.38 |         0.26 |               0.34 |               0.36 |              0 |          0 |
| Phone                |     0.34 |         0.22 |               0.38 |               0.36 |              0 |          0 |
| Email                |     0.28 |         0.12 |               0.32 |               0.46 |              0 |          0 |
| Relatives            |     0.5  |         0.4  |               0.48 |               0.52 |              0 |          0 |
| Associates           |     0.46 |         0.4  |               0.46 |               0.54 |              0 |          0 |
| Court/public records |     0.14 |         0.08 |               0.08 |               0.14 |              0 |          0 |

Mean cell score by site:

| site             |   mean score |
|:-----------------|-------------:|
| Spokeo           |         0.84 |
| Whitepages       |         0.6  |
| TruePeopleSearch |         0.86 |
| FastPeopleSearch |         0.97 |
| BeenVerified     |         0.72 |
| Intelius         |         0.8  |


## A2 Tenure gradient

Exposure score by tenure band:

| tenure_band   |   n |   median |   mean |   sd |
|:--------------|----:|---------:|-------:|-----:|
| Under 3 years |  19 |     27   |   26.3 |  9.5 |
| 3 to 10 years |  18 |     33.5 |   32.3 | 12.8 |
| Over 10 years |  13 |     46   |   45.6 |  7   |

Kruskal–Wallis H = 19.63, p = 0.0001

Pairwise (later band minus earlier band):

| comparison | Mann–Whitney p (Holm) | Cliff's delta [95% CI] |
|---|---|---|
| 3 to 10 years vs Under 3 years | 0.1284 | 0.30 [-0.06, 0.64] |
| Over 10 years vs Under 3 years | 0.0001 | 0.89 [0.67, 1.00] |
| Over 10 years vs 3 to 10 years | 0.0031 | 0.68 [0.36, 0.94] |

OLS (HC3): exposure_score ~ tenure_years + C(occupation_band) + household_size + own_record

|                                        |   coef |   2.5% |   97.5% |     p |
|:---------------------------------------|-------:|-------:|--------:|------:|
| Intercept                              | 18.506 |  6.613 |  30.399 | 0.002 |
| C(occupation_band)[T.Other]            |  8.919 | -4.223 |  22.061 | 0.183 |
| C(occupation_band)[T.Professional]     |  5.677 | -6.674 |  18.029 | 0.368 |
| C(occupation_band)[T.Small business]   |  5.533 | -5.95  |  17.016 | 0.345 |
| C(occupation_band)[T.Warehouse & food] |  2.262 | -9.821 |  14.345 | 0.714 |
| tenure_years                           |  0.754 |  0.23  |   1.278 | 0.005 |
| household_size                         |  0.035 | -1.367 |   1.437 | 0.961 |
| own_record                             |  5.723 | -1.624 |  13.069 | 0.127 |

R² = 0.386, n = 50


## A3 Awareness versus exposure

- Spearman rho, A11 predicted findability × address sites (score 2): 0.10 (p = 0.496)
- Spearman rho, A12 predicted relatives × relatives sites (score 2): -0.17 (p = 0.238)
- Spearman rho, awareness index × exposure score: 0.49 (p = 0.000)

Prediction gap (standardised address exposure minus standardised predicted findability; positive = more exposed than expected):

| tenure_band   |   n |   median |   mean |
|:--------------|----:|---------:|-------:|
| Under 3 years |  19 |     0.06 |  -0.15 |
| 3 to 10 years |  18 |     0.06 |   0.08 |
| Over 10 years |  13 |     0.06 |   0.12 |

Kruskal–Wallis across tenure bands: H = 0.32, p = 0.8520

Predicted findability (rows, 1 very unlikely … 4 very likely) × number of sites with accurate address (columns):

|   predicted_findability |   0 |   1 |   2 |   3 |   4 |
|------------------------:|----:|----:|----:|----:|----:|
|                       1 |   3 |   4 |   7 |   7 |   0 |
|                       2 |   5 |   2 |   4 |   1 |   1 |
|                       3 |   3 |   1 |   2 |   5 |   3 |
|                       4 |   0 |   0 |   2 |   0 |   0 |


## A6.1 Site-field co-exposure network

Nodes: 28 site-field combinations with at least one participant scoring 2; edges kept where at least 4 participants (9%) are co-exposed; 280 edges.
Louvain communities: 4, modularity 0.054.

- Community 1 (11 nodes): FPS:address, FPS:associates, FPS:email, FPS:past addr, FPS:phone, FPS:relatives, TPS:address, TPS:associates, TPS:email, TPS:phone, TPS:relatives
- Community 2 (9 nodes): Spokeo:records, TPS:past addr, Whitepages:address, Whitepages:associates, Whitepages:email, Whitepages:past addr, Whitepages:phone, Whitepages:records, Whitepages:relatives
- Community 3 (7 nodes): FPS:records, Spokeo:address, Spokeo:associates, Spokeo:email, Spokeo:past addr, Spokeo:phone, Spokeo:relatives
- Community 4 (1 nodes): TPS:records

Highest degree centrality: FPS:email (0.93), Spokeo:phone (0.93), FPS:address (0.89), Whitepages:relatives (0.89), Whitepages:associates (0.89), Whitepages:past addr (0.89), Whitepages:phone (0.89), Spokeo:associates (0.85)


## A6.2 Institution data-flow graph

Institutions ranked by participants mentioning them, with the share of their events for which any downstream holder was named:

| event_type               |   events |   participants |   known-recipient ratio |
|:-------------------------|---------:|---------------:|------------------------:|
| Driver's license         |       29 |             26 |                    0.55 |
| Government office        |       33 |             23 |                    0.7  |
| School enrollment        |       24 |             22 |                    0.25 |
| Phone plan               |       30 |             22 |                    0.1  |
| Job-site resume          |       27 |             21 |                    0.37 |
| Utility account          |       26 |             21 |                    0.12 |
| Bank account             |       22 |             21 |                    0.55 |
| Job / payroll            |       27 |             19 |                    0.33 |
| Car purchase / insurance |       25 |             19 |                    0.48 |
| Remittance               |       25 |             19 |                    0.16 |
| Religious community      |       23 |             18 |                    0.13 |
| Other                    |       20 |             17 |                    0.3  |
| Resettlement agency      |       23 |             17 |                    0.3  |
| Clinic / hospital        |       21 |             16 |                    0.29 |
| Lease / housing          |       23 |             16 |                    0.22 |
| Immigration attorney     |       16 |             13 |                    0.69 |

Overall known-recipient ratio: 0.35 across 394 events from 50 participants.


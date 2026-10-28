# Privacy by Request: Immigrant Settlement and the Limits of Individual Control in the Data Broker Economy

**Research package: protocol, instruments, codebook, synthetic data and analysis code for a mixed-methods study of data-broker exposure among immigrant adults in the Twin Cities, Minnesota.**

Principal investigator: Endalkachew H. Chala, PhD (Community Fellow, Center for an Informed Public, University of Washington)
ORCID: [0000-0001-6210-6706](https://orcid.org/0000-0001-6210-6706)
Status: data collection in progress (October 2026). Working title of the article: *Delete Me, If You Can Afford It: Data Brokers, Privacy Labor, and the Immigrant Exposure Gap*.

---

## 1. Research problem

People-search sites and the data brokers behind them assemble dossiers on United States residents from public records, commercial transactions and platform activity, and sell them to anyone with a search box or a subscription. Opting out is lawful, site by site and request by request; paid removal services (DeleteMe, Incogni, Optery and others) exist precisely because the task is unmanageable for an individual. The remedy that United States law provides, in other words, is privacy by request.

This study asks what privacy by request means for people whose settlement in the United States requires them to generate records. Leases, utility accounts, driver's licences, payroll, remittance transfers and job-site résumés are not optional for a newly arrived adult; each lawfully feeds the same pipeline. The study treats this condition as **compulsory exposure**: exposure produced by the convergence of compulsion (records one must create), participation (platform activity in community networks) and aspiration (job-seeking) in the same commercial databases.

The central construct is **communicative access to privacy**: whether a person (a) recognises that a remedy exists, (b) can execute its procedure in a language and format available to them, and (c) is substantively covered by it, given that the removal market reaches the consumer tier of people-search sites and not the investigative tier (CLEAR, Accurint, TRAC) used by employers, landlords and enforcement. The study deliberately avoids a knowledge-deficit framing: the question is not what immigrants fail to know but what the remedy fails to reach.

## 2. Research objective

To measure the actual findability of immigrant adults in consumer people-search databases, to compare it with their own expectations and awareness, and to trace the settlement-era disclosures through which that findability was produced, in order to specify how the structure of privacy by request distributes exposure by tenure, occupation and language.

## 3. Research questions

| | Question | Primary data |
|---|---|---|
| RQ1 | How exposed are immigrant adults in consumer people-search databases, by field (address, past addresses, phone, email, relatives, associates, public records) and by site, and how does exposure vary with tenure in the United States and occupation band? | Exposure audit (6 sites × 7 fields, 0/1/2) |
| RQ2 | How does measured exposure compare with participants' pre-lookup predictions of their own findability and with their awareness of brokers, people-search sites, removal services and deletion laws? | Awareness instrument (18 items) administered before any lookup |
| RQ3 | Through which settlement-era disclosure events was the exposed information produced, and for how many of these events can participants name any downstream holder of the data? | Settlement-timeline exercise |
| RQ4 | How do platform participation and job-site résumé posting contribute to exposure, and what temporality and audience models do participants hold for these channels? | Platform-use and job-site modules |
| RQ5 | How do participants interpret exposure once shown it: in what vocabulary, with what imagined searcher, at what unit of harm (individual, household, community), and with what repertoire of response? | Lookup reactions; semi-structured interviews (subset) |

## 4. Design

Convergent mixed-methods design with a qualitative lead, conducted in single sessions of 60 to 90 minutes.

**Sample.** 40 to 60 immigrant adults (18+) in the Minneapolis–Saint Paul metropolitan area, recruited through community organisations other than the investigator's employer, stratified by tenure in the United States (under 3 years; 3 to 10 years; over 10 years) and by occupation band (care and service; warehouse and food; small business; professional; other). A subset of 15 to 20 participants completes a longer interview on meaning and language. The comparison of interest is the tenure gradient within the immigrant sample; no non-immigrant comparison group is recruited. Immigration status is never asked and never recorded.

**Session sequence** (order is fixed; the awareness instrument always precedes any lookup):

1. Intake (strata only; no identifying free text).
2. Awareness instrument, 18 items (`instruments/awareness_instrument.md`).
3. Settlement-timeline exercise: disclosure events in the first two years after arrival.
4. Platform-use module, including an optional consented walkthrough of the participant's Off-Facebook Activity page.
5. Job-site module, including a check of résumé visibility settings in the participant's own account.
6. Exposure audit: consented lookup of the participant's name and city on six people-search sites, scored with the participant present (`protocol/exposure_audit.md`).
7. Lookup reactions, recorded per element shown.
8. Debrief with an opt-out guide in the participant's language; stop rule for distress.
9. Longer interview (subset), transcribed and coded (`codebook/`).

**Primary quantitative measure.** The exposure score: six sites (Spokeo, Whitepages, TruePeopleSearch, FastPeopleSearch, BeenVerified, Intelius) × seven fields, each scored 0 (not shown), 1 (partial, stale or ambiguous) or 2 (accurate and current, confirmed by the participant), summed to a range of 0 to 84. Site content is never copied; only the score is recorded.

**Analytic positions.** Participants are classified into four positions derived from tenure, awareness index and own-name records: settled and unknowing; settled and informed; recent and on the record; recent and off the record.

## 5. Analysis plan

Pre-specified in `analysis/ANALYSIS_PLAN.md`. In brief:

- **Descriptive.** Distribution of exposure scores; per-site and per-field prevalence of accurate exposure (score 2); exposure heatmap ordered by tenure.
- **Tenure gradient (RQ1).** Exposure score by tenure band (Kruskal–Wallis; pairwise Mann–Whitney with Holm correction) and a linear model with tenure in years, occupation band and household size. Effect sizes and 95% confidence intervals are reported; the sample is powered for large effects only.
- **Awareness versus exposure (RQ2).** Predicted findability (1 to 4) against measured address exposure; awareness index against exposure score; the prediction gap as the operational measure of communicative access.
- **Channel contributions (RQ3, RQ4).** Exposure regressed on the count of compulsory-record events, platform hours per day, and public résumé status; share of timeline events for which a downstream holder was named.
- **Network analyses.** (a) A two-mode participant × site-field network projected to a site-field co-exposure network, with community detection to identify exposure bundles (household bundle versus contact bundle). (b) A directed institution → recipient data-flow graph built from the settlement timeline, weighted by participant counts, with the known-recipient ratio per institution. No network of real persons is ever constructed.
- **Qualitative.** Deductive coding of interviews against the codebook (imagined searcher, imagined audience, unit of harm, vocabulary gloss, response repertoire); 25% double-coded with agreement reported.
- **Reliability.** A random 20% of exposure audits re-scored from session notes by a second coder; weighted kappa reported.

All figures in the article are regenerated by `analysis/run_all.py` from the released file; the synthetic dataset in `data/synthetic/` lets anyone run the pipeline end to end.

## 6. Ethics

- Approved protocol: see `protocol/` (IRB number to be added on approval).
- The investigator's employer and its clients are excluded from the sample. The investigator's role as an intermediary who prepares job-site résumés for immigrant clients is declared and treated reflexively.
- Lookups are performed only during a consented session, with the participant watching the screen and confirming which result, if any, is theirs. Lookups are never batched, pre-run or repeated outside sessions. The researcher-operated lookup tool (`tools/lookup_assistant.py`) opens one site at a time in a visible browser, proposes scores from page text, and records only the researcher's confirmed 0/1/2 scores against the participant ID; it never stores the name.
- A stop rule applies if a participant shows distress; every participant receives an opt-out guide in their language and is walked through one opt-out request.
- Participants approve any quotation before publication.
- Immigration status, country of origin, full address, date of birth and employer names are never recorded.

## 7. Data tiers

| Tier | Contents | Where |
|---|---|---|
| **Open** | Protocol, instruments, codebook, analysis code, aggregate figures, synthetic dataset | This repository; Zenodo DOI on release |
| **Restricted** | De-identified participant file: tenure band (not years), occupation band, region collapsed to four categories, exposure score and sub-scores, awareness items, platform and job-site indicators, interview codes; cells under k = 5 suppressed | Under data-use agreement, on request to the PI |
| **Never released** | Exposure grid (per-site, per-field scores), settlement timelines, lookup-reaction free text, transcripts, screenshots, the ID-to-name key | Encrypted, PI only; destroyed at study close per protocol |

`data/raw/` and `data/restricted/` are git-ignored. Nothing in this repository contains or can be used to recover a participant's identity.

## 8. Repository structure

```
README.md
CITATION.cff
LICENSE
protocol/
  session_protocol.md          full session script, consent flow, stop rule, debrief
  exposure_audit.md            the six sites, seven fields, scoring rules, namesake handling
  data_management_plan.md      tiers, encryption, retention, destruction
instruments/
  awareness_instrument.md      18-item pre-lookup instrument with coding
  settlement_timeline.md       timeline exercise and event types
  platform_and_jobsite_modules.md
  interview_guide.md           semi-structured guide for the subset
  optout_guide_template.md     participant-facing opt-out guide (to be translated)
codebook/
  codebook.csv                 every variable: sheet, type, allowed values, source, release tier, definition
  interview_codes.md           deductive code definitions
data/
  synthetic/                   generated by make_synthetic.py; schema-identical, no real values
  raw/                         (git-ignored) session workbook
  restricted/                  (git-ignored) de-identified file for DUA release
analysis/
  ANALYSIS_PLAN.md             pre-specified analyses
  make_synthetic.py            synthetic data generator
  01_descriptives.py           exposure distribution, per-site and per-field prevalence, heatmap
  02_tenure_gradient.py        tenure-band comparison and model
  03_awareness_vs_exposure.py  prediction gap
  04_network_coexposure.py     site-field co-exposure network
  05_network_dataflow.py       institution data-flow graph
  run_all.py                   runs the pipeline on synthetic or real data
figures/                       regenerated outputs (synthetic by default)
tools/
  lookup_assistant.py          researcher-operated session-time lookup tool
  README.md
```

## 9. Reproducing the figures

```
pip install -r requirements.txt
python analysis/make_synthetic.py            # writes data/synthetic/*.csv
python analysis/run_all.py --data synthetic  # writes figures/*.png and figures/tables.md
```

To run on the real de-identified file (restricted tier, PI only): `python analysis/run_all.py --data restricted`.

## 10. Theoretical grounding

The design draws on Scott on legibility, Cohen on the biopolitical public domain, Nissenbaum on contextual integrity and transmission principles, Solove on the limits of privacy self-management, Viljoen on relational data, Marwick and boyd on networked privacy, Draper and Turow on digital resignation, Couldry and Mejias on data colonialism, Gandy on the panoptic sort, Fineman on vulnerability, and Mayer-Schönberger on deletion. The full literature review is in the article manuscript, not in this repository.

## 11. Citation

See `CITATION.cff`. Until a Zenodo DOI is minted, cite as:

Chala, E. H. (2026). *Privacy by Request: research package* (Version 0.2) [Protocol, instruments, code and synthetic data]. GitHub. https://github.com/Endalk-Chala/privacy-by-request

## 12. Licence

Code: MIT. Protocol, instruments, codebook and documentation: CC BY 4.0. Synthetic data: CC0.

## 13. Contact

Endalkachew H. Chala, endalk2006@gmail.com. Requests for the restricted-tier file should describe the intended analysis and the applicant's institutional ethics approval.

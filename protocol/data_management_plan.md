# Data management plan

## Identifiers

- The participant ID (P01...) is the only identifier in any data file.
- The ID-to-name key is a single encrypted file held by the PI, stored separately from all data, and destroyed at study close.
- No data file ever contains: name, immigration status, country of origin, full address, date of birth, employer name, SSN/ITIN, or free text that could identify a person in a small community.

## Collection

- The session workbook (`exposure_study_data_collection.xlsx`) is the sole collection instrument; one row per participant per sheet, coded fields only.
- The lookup tool writes scores and dates only. The name is typed at a prompt, used to open six search pages, and discarded when the browser closes; Playwright launches a non-persistent browser context, so no history or cookies survive the run.
- Terminal windows are closed at the end of each session.

## Storage

- Workbook and key: encrypted volume on the PI's laptop; backed up to an encrypted institutional store.
- Audio and transcripts: encrypted; transcripts pseudonymised before coding.
- Screenshots: not taken unless the protocol amendment is approved; if taken, stored with the key and deleted at study close.

## Release tiers

| Tier | Contents | Conditions |
|---|---|---|
| Open | Protocol, instruments, codebook, analysis code, aggregate figures and tables, synthetic dataset | Public: GitHub and Zenodo |
| Restricted | De-identified participant file: tenure band (tenure in years removed), occupation band, region in four categories, exposure score and sub-scores, awareness items, platform and job-site indicators, interview codes; any cell with fewer than five participants merged or suppressed | Data-use agreement; applicant's ethics approval; no re-identification attempts; no linkage |
| Never | Exposure grid, settlement timelines, lookup-reaction free text, transcripts, audio, screenshots, the key | PI only |

## Retention and destruction

- Restricted-tier file: retained five years after publication, then destroyed.
- Never-tier material: destroyed at study close (defined as publication of the main article or three years after the last session, whichever is earlier).
- Participants may withdraw within 30 days of their session; their rows are deleted from every sheet and the key.

## Repository hygiene

`data/raw/`, `data/restricted/`, `*.xlsx`, `exposure_grid_rows.csv`, `recovery_*.csv` and `captures/` are git-ignored. A pre-commit check (`tools/check_no_pii.py`) refuses commits containing a pattern that looks like a personal name next to a participant ID.

# Lookup assistant for the exposure study

A session-time helper that runs the six people-search lookups for one participant, proposes the 0/1/2 scores for the seven fields, and writes the 42 rows of the Exposure_Grid sheet. It is a convenience for the researcher, not a crawler: it runs one person at a time, in a visible browser, with you pressing Enter at each site, and it never stores the name.

## Setup (once, in PowerShell or Command Prompt)

```
cd <your local copy>\tools
pip install playwright openpyxl
python -m playwright install chromium
```

## Before the first real session

1. Add one sentence to the IRB protocol: "During the session the researcher uses a script that opens the six sites' search pages in a browser and records the researcher's 0/1/2 scores; optional screenshots are stored encrypted in the restricted tier and deleted at study close."
2. Check the URL patterns with the built-in fictional name: `python lookup_assistant.py --check-urls`. It opens each site for "Dawit Example, Saint Paul, MN" and asks whether the page is a results page. If one is not, edit that site's line in `build_url()` or navigate by hand when the script pauses during sessions.
3. Run the dry run to see the scoring flow with no browser: `python lookup_assistant.py --dry-run`

## In the session

```
python lookup_assistant.py
python lookup_assistant.py --screenshots                     # keep PNGs in captures\<ID>\
python lookup_assistant.py --append-xlsx exposure_study_data_collection.xlsx
```

The script asks for the participant ID, name, city and state at the prompt. For each site it opens the search, waits for you (clear any CAPTCHA by hand), reads the page text, proposes scores with a one-line reason, and lets you accept with Enter or type 0/1/2. Scores and an optional note go to `exposure_grid_rows.csv` (and to the workbook if you pass `--append-xlsx`).

## Scoring rules the script uses

- Free sites (Spokeo, Whitepages, TruePeopleSearch, FastPeopleSearch): street-address, phone and email patterns, and "relatives" / "associates" / records keywords in the page text. Two or more distinct addresses means past addresses. Many surname hits caps everything at 1 with a namesake warning, because the page probably lists several people.
- Paywalled sites (BeenVerified, Intelius): only whether a teaser says a record exists. 1 if so, 0 if not. The script cannot see fields behind the paywall; score them yourself if you have a subscription.
- The proposal is a starting point. Your judgment in the room, with the participant confirming which card is theirs, is the score.

## What it will not do

Run without you present, batch several participants, bypass CAPTCHAs or paywalls, or keep the search name. Screenshots are copies of personal data: treat them as restricted-tier material or do not enable them.

## Data files in this folder

`exposure_grid_rows.csv` and anything under `captures\` contain study data. Keep them out of any public repository (the `.gitignore` here already excludes them).

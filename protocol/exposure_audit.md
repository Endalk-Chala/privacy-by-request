# Exposure audit: sites, fields, scoring rules

## Sites (consumer tier)

| Site | Access | What the audit can see |
|---|---|---|
| Spokeo | free results page, paid report | summary card: address, age, relatives; some phone and email |
| Whitepages | free results page, paid report | address, phone, relatives; aggressive bot detection |
| TruePeopleSearch | free, full | address history, phones, emails, relatives, associates |
| FastPeopleSearch | free, full | as TruePeopleSearch |
| BeenVerified | paywalled; teaser only | whether a record exists |
| Intelius | paywalled; teaser only | whether a record exists |

The two paywalled sites are scored on the teaser only unless the investigator holds a subscription; this is recorded in the method memo. The investigative tier (CLEAR, Accurint, TRAC) is not searched; a redacted example report is shown in the debrief instead.

## Fields

1. Current address
2. Past addresses
3. Phone
4. Email
5. Relatives
6. Associates
7. Court or public records

## Scoring

Each site × field cell receives one score, decided by the investigator with the participant present:

- **0** The field is not shown for this person.
- **1** Partial, stale or ambiguous: a paywall teaser; a truncated value; an outdated address the participant recognises as a former one listed as current; or the field appears on a card the participant cannot confirm as theirs among namesakes.
- **2** Accurate and current, confirmed by the participant as theirs.

Past addresses scores 2 only when two or more former addresses are listed and the participant confirms them; one confirmed former address scores 1. Relatives and associates score 2 when at least one named person is confirmed by the participant as a real relative or associate; the names are never recorded, only the score.

The exposure score is the sum over the 42 cells (0 to 84). Sub-scores: `address_sites` (number of sites scoring 2 on current address), `relatives_sites` (number of sites scoring 2 on relatives).

## Namesake rule

Common names return many cards. The participant identifies their own card; if they cannot, every field on that site is capped at 1 and the note records "namesake ambiguity". The investigator never clicks into a card that the participant has not identified as theirs.

## Procedure

1. Launch `tools/lookup_assistant.py` with the participant ID; enter name and city at the prompts (never on the command line).
2. For each site in turn the tool opens the search-results page in a visible browser. Wait until the page has fully loaded; clear any CAPTCHA by hand. Do not proceed on a homepage, error page or consent wall.
3. With the participant, identify their card. Read the tool's proposed scores against the page and accept or correct them, seven digits per site.
4. Optional note per site: method only (for example "CAPTCHA; searched manually", "namesake ambiguity"). Never content.
5. After the sixth site the tool writes 42 rows to the Exposure_Grid sheet under the participant ID, dated.

## What is never done

- Lookups outside a consented session, before consent, or for anyone not present.
- Batched or repeated lookups.
- Copying, screenshotting (unless the approved amendment permits it) or reading aloud any value from a page.
- Searching relatives or associates shown on a card.
- Searching the investigative tier.

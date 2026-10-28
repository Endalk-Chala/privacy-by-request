# Session protocol

Version 0.2, October 2026. One participant per session; 60 to 90 minutes; in person; in the participant's preferred language where the investigator is able to conduct it (Amharic, Afan Oromo, English) or with an interpreter otherwise.

## 1. Before the session

- Confirm eligibility: adult (18+), born outside the United States, resident of the Minneapolis–Saint Paul metropolitan area, not a client or employee of the investigator's employer.
- Assign a participant ID (P01, P02, ...). Record the ID-to-name mapping only in the encrypted key file. The ID is the only identifier used in any data file.
- Prepare: consent form in the participant's language; the awareness instrument; the timeline sheet; the income-band card; the opt-out guide; the stop-rule card; a laptop with the lookup tool installed and no browser sessions open.

## 2. Consent

Read the consent form aloud or have the participant read it. Cover, in plain language:

- what will happen, in the order it will happen, including that the investigator will search the participant's name on six public people-search websites while the participant watches;
- that nothing from those websites is copied or saved; only a score is recorded;
- that the participant can stop at any point, skip any part, and withdraw within 30 days;
- that immigration status, country, address, date of birth and employer will not be asked;
- the three separate consents: (a) participation; (b) release of de-identified scores to the restricted tier; (c) approval of quotations before publication.

Record consent decisions as 0/1 in the Participants sheet. Do not begin the awareness instrument until (a) is given.

## 3. Intake (Participants sheet)

Strata only: tenure in years (one decimal), occupation band, region of origin (four categories), education band, income band from the card, household size. No free text.

## 4. Awareness instrument

Administer all 18 items (`instruments/awareness_instrument.md`) **before** any lookup, any mention of what people-search sites show, and any mention of removal services. Read items verbatim. Record codes only.

## 5. Settlement-timeline exercise

Ask the participant to recall the first two years after arrival and to list, month by month as far as they can, each occasion on which they gave their name, address, date of birth or SSN/ITIN to an organisation (`instruments/settlement_timeline.md`). For each event, ask whether they know of anyone else who later held that information, and record Yes/No and the type of recipient named. Do not suggest recipients.

## 6. Platform-use and job-site modules

Administer per `instruments/platform_and_jobsite_modules.md`. The Off-Facebook Activity walkthrough and the job-site visibility check are performed on the participant's own device, by the participant, with the investigator looking on; the investigator never logs in to a participant's account.

## 7. Exposure audit

Follow `protocol/exposure_audit.md` exactly. Screen faces the participant throughout. Score each field with the participant confirming which result is theirs. Stop immediately if the stop rule is triggered.

## 8. Lookup reactions

For each element shown (people-search lookup, platform data, résumé search, redacted investigative-tier example), record: whether shown, what the participant commented on first, the dominant reaction code, the distress flag, whether stopped early, and a quote ID if a quotation was noted for later approval.

## 9. Debrief

- Explain what the sites are, where the information comes from, and that removal is possible but site by site.
- Give the opt-out guide in the participant's language and walk through one opt-out request together on a site of the participant's choosing. Record that this was done.
- Explain the paid removal services, their cost, and what they do not cover (the investigative tier).
- Give the contact card for questions and withdrawal.

## 10. Stop rule

If the participant shows distress (tearfulness, agitation, expressed fear for self or family, request to stop): stop the lookup, close the browser, set `distress_flag = 1` and `stopped_early = 1`, move directly to the debrief and opt-out guide, and offer to end the session. Do not resume the lookup in that session. Note what was shown at the point of stopping (element only, no content).

## 11. After the session

- Enter remaining codes the same day. Close the lookup tool and the terminal.
- Verify that no file in the project folder contains the participant's name. Screenshots, if the protocol amendment permitting them is approved, are moved to the encrypted restricted store or deleted.
- Write a short method memo: which sites loaded, any CAPTCHA, any namesake ambiguity, anything the instrument did not capture.

## 12. Interview subset

Participants who consent and whose position cell is under-represented are invited to a 45-minute follow-up interview (`instruments/interview_guide.md`), audio-recorded, transcribed, and coded per `codebook/interview_codes.md`. Transcripts are never released.

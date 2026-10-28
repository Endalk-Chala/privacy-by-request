# Settlement-timeline exercise

Purpose: to reconstruct the disclosure events of the first two years after arrival and to measure how many of them the participant can connect to any downstream holder of their data (RQ3). The exercise is also the empirical basis of the institution data-flow network.

## Prompt

"Think back to your first two years here. I am going to ask about the times you gave your name, address, date of birth or Social Security or tax number to an organisation. We will go roughly month by month. There are no wrong answers and you can skip anything."

## For each event, record (Settlement_Timeline sheet)

| Column | Values |
|---|---|
| event_no | 1, 2, 3 ... in the order recalled |
| month_after_arrival | 0 to 24 (best estimate) |
| event_type | one of the 16 types below |
| gave_name, gave_address, gave_dob, gave_ssn_itin | 0/1 each |
| named_downstream_holder | Yes if the participant, unprompted, names anyone beyond the first party who later held the information; otherwise No |
| named_recipient_type | if Yes: government / credit bureau / data broker or website / employer / landlord / other; if No: blank |
| confidence | 1 unsure / 2 fairly sure / 3 certain |
| intermediary_type | who helped: none / relative / caseworker / resettlement agency / employer / attorney / other |
| notes | method only |

## Event types

Lease or housing · Utility account · Phone plan · Bank account · Driver's licence · Job or payroll · Remittance · Clinic or hospital · School enrolment · Religious community · Government office · Car purchase or insurance · Job-site résumé · Immigration attorney · Resettlement agency · Other

## Probes (use only after the participant has finished recalling)

- "Did anyone help you fill that in?" (intermediary_type)
- "Do you know whether anyone else got that information afterwards?" (named_downstream_holder; do not suggest names)
- "Was that in your name or someone else's?" (feeds `own_record` on the Participants sheet: 1 if a lease or utility account is in the participant's own name)

## Derived measures

- `timeline_events`: number of events.
- `known_recipients`: events with named_downstream_holder = Yes.
- `known_recipient_ratio`: known_recipients / timeline_events.
- Per institution (aggregate only): number of participants mentioning it; share naming a downstream holder. These two numbers per institution are the only timeline data ever released.

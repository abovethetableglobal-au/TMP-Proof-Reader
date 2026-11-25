# MRWA Sources Integration & Submission-to-Final Workflow — v0.1 (draft, 2026-11-25)

Status: **Ready for user review**. Evidence labels per Master Prompt §18.2.

## 1. MRWA sources supplied by Owner (downloaded and read 2026-11-25 — verified fact unless noted)

| # | Document | Format | What it gives the check | Use in TMP Check |
|---|---|---|---|---|
| 1 | Generic workzone TGSs (AS 1742.3 signs) | PDF 27 pp | Index of MRWA generic TGS numbers + issue dates (e.g. 001–… dated 6/08/2014); preface: daylight works on Highways/Main Roads only, not a replacement for TMPs | **Reference library**: validate any cited generic TGS number/date/description; flag use outside stated scope (night works, local roads) as Query |
| 2 | Example Generic TGSs (Mar 2026) | PDF 15 pp | Illustrative example TGSs (e.g. STLI-001), title block layout, AGTTM table references; states COP + AGTTM remain authoritative | **Pass D benchmark**: expected title-block fields; NOT a compliance source (illustrative only) |
| 3 / 6 | Generic vs site-specific TMP checklist (two links, near-identical Word files) | DOC 1 p | 13 triggers; any "yes" = site-specific TMP; generic TMPs reviewed ≥ every 12 months | **Rule WA-GEN-CHK-001** (draft) |
| 4 | Generic TGS Site Suitability Assessment (**Proposed update**) | PDF 1 p | 9 suitability questions; tied to Daily TM Diary | **Rule WA-GEN-TGS-001** (draft). Assumption: may not yet be in force — Tara to confirm |
| 5 | Events — Generic Traffic Control Diagrams | PPT (2015) | Event TCDs | **Out of current scope** (works-on-roads TMPs). Park for an "Events" product line |
| 7 | Generic workzone TGSs — MMS | PDF 22 pp | Same index for multi-message-sign variants | Reference library, as #1 |
| — | Working on roads web page | HTML | Hub for templates and checklists | Source register monitor: re-check quarterly for new editions |

Not stored in the repo (MRWA copyright); the engine stores only rule paraphrases and an index of TGS numbers/dates/titles with source links.

## 2. How they enter the check

1. **Classify** (new step 0): read the TMP — generic or site-specific? road authority? uses generic TGSs?
2. **Generic TMP** → run WA-GEN-CHK-001: extract hours, length, vph, intersections, rail, signals, detours, path users; any trigger present → *Potential issue (Major): site-specific TMP may be required*; data absent → *Unable to verify*.
3. **Generic TGS cited** → look up number in TGS index (#1/#7): mismatch of number, date or description → Moderate; missing suitability assessment → WA-GEN-TGS-001.
4. **Jurisdiction guard** (done today): interstate agency in the TMP = Moderate finding; interstate wording in our own output = blocked to Query for rewrite.

## 3. End-to-end workflow: client submission → finalised content

| Stage | Who | Output | Gate / control |
|---|---|---|---|
| 1 Submit | Client | TMP PDF + TGSs + intake form (road, authority, generic/site-specific, dates, generic TGSs used) | Credit reserved (not consumed); data-handling consent |
| 2 Intake QA | Engine | Files legible, pages count, TGS pages detected; intake vs document mismatches | Reject unreadable files — no credit used |
| 3 Classify | Engine | TMP type, authority, road class, applicable rule set | Low confidence → ask client one question |
| 4 Checks | Engine | Deterministic → LLM passes A–D → rule set E (COP + MRWA checklists + TGS index) | Evidence validation; jurisdiction guard; no citation → Query |
| 5 Draft | Engine | Draft findings report + annotated rendition (original untouched) | Watermarked DRAFT |
| 6 Review | Client's accredited reviewer (A-15) | Accept / edit / reject each finding; add own | Every finding dispositioned; no Critical released unsupported |
| 7 Final | Engine | Final report + annotated PDF + disposition log | Credit consumed; reviewer named on report |
| 8 Revise loop (optional) | Client | Re-submit revised TMP → diff vs previous, confirm closures | Pricing TBD (P-12) |
| 9 Learn | AI-PM | Reviewer edits/rejections → rule tuning, false-positive log | No training on customer data |

## 4. Open items
- P-12 pricing (Tara: $149 undersells; checks take 5+ h manually) — Owner decision.
- Tara to review WA-GEN-CHK-001 / WA-GEN-TGS-001 and confirm #4 is in force.
- Build TGS index extractor from #1/#7 (Pass E support) — next G4 task.

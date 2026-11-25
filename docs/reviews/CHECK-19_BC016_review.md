# Check 19 — TMP BC 016 (live TMP, A-41 exception): output review v0.1

Review type: simulated (AI-PM only). Inputs: findings.json, report PDF (21 pp), annotated PDF (81 pp).

| Metric | Value |
|---|---|
| Pages | 81 |
| Passes | A–D ×2 + rules |
| AI cost | US$7.29 (US$0.09/page; check 14 was US$6.10 for 64 pp) |
| Findings | 192: 0 Critical, 17 Major, 42 Moderate, 102 Minor, 31 Query |
| By category | A 70, B 31, C 52, D 38, E 1 |
| Raised by more than one pass | 76 (40%), already merged |
| Missing action | 0 |

## Observations
- No Critical findings. The Majors are specific, cite the TMP's own text and pages, and give actions (e.g. Transperth endorsement claimed but Appendix E is empty; bus stop 28509 conflict; no crane exclusion zone on the TGS).
- 11 separate "TBA" rule findings. Group them into one finding that lists the pages (Minor, noise).
- [385] combines two unrelated issues (missing Appendix G + a repeated sentence). Split them.
- Some Queries are plain proofreading errors (e.g. [366] 'to' → 'a'). The export does not say why they are Queries (most likely the quote was not located).

## Defects
| ID | Defect | Status |
|---|---|---|
| DEF-C19-1 | The export lacks `outcome`, `section` and the reason a finding was held as a Query | Partly fixed: `outcome`/`section` added to the export. The hold reason is not stored in the DB; open |
| DEF-C19-2 | The export has no `timings` / `processing_seconds`, so the PC portal is running code from before 5cfc73a | Owner: `git pull` on the PC |
| DEF-C19-3 | Repeated PH-TBA findings are not grouped | Open |
| DEF-C19-4 | Compound findings (two issues in one) | Open: prompt rule "one issue per finding" |

| DEF-C19-5 | Annotated copy: one 'F-xxx (related) — see report' label per finding per related page, stacked down the top-right corner (up to 19 on p78), covering TMP text and TGS content. 641 labels in total | Fixed: one combined 'Also affects this page' note per page (641 → 268 labels; checked on p78) |

## Outputs check
- Report: all 192 F-numbers present; summary counts match the export; the draft banner and reviewer gate are present.
- Annotated copy: all 192 F-numbers present; 170 highlighted on the TMP text, 22 as margin notes (mostly VISUAL/TGS findings). DEF-C14 highlighting confirmed working.
- PDF download works; on the Owner's PC Windows labels PDFs "Chrome HTML Document" (file association only).

## Still needed
Tara's dispositions for precision.

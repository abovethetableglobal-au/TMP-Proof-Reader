# BENCH-02 — Full engine (rules + AI passes A–D) vs reference findings (REF-01)

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Document | REF-01 source TMP SU026 (61 pp incl. TGS 01–03), run in the local portal on the Owner's PC (A-18) |
| Reference | REF-01 proofread report, confirmed correct by WTGTM (A-19) |
| Engine | `det_checks` 0.2 + `llm_checks` passes A,B,C,D + cross-check duplicate merging (portal 0.2) |
| Data | Findings export `check-5-findings.json` (git-ignored `customer-docs/`) |
| Scorer | AI-PM — **simulated, not independent** (§5.3). Matching by page + issue meaning. Needs Tara's confirmation before G5 use |
| Status | Under review — actions 1–3 implemented 2026-11-20, BENCH-03 pending |

## Headline
| Measure | Result |
|---|---|
| AI cost | **US$3.33** (≈ A$5) for 61 pages |
| Findings raised | 293 raw → **211** after merging duplicates |
| Reference items found (recall) | **97 of 110** scored rows (**88%**) |
| Findings matching a reference item | 141 (several findings per item — see Noise) |
| Disagree with reference (likely false) | 3 |
| Not in reference — substantive, plausible | 31 |
| Not in reference — style nits | 30 |
| Duplicates of matched items / Owner-excluded type | 6 |
| Critical findings | 0 (reference has none) |
| Est. reviewer time at 20–30 s/finding | **70–105 min** vs 45 min target (R-03) — **not met** |

BENCH-01 (rules only): 9/26 leftovers (35%). BENCH-02: 25/26 leftovers (96%).

## Recall by reference section
| Section | Reference rows | Found | Recall | Missed |
|---|---|---|---|---|
| 1 Typos and grammar | 44 | 35 | 80% | heading spacing p9; "upto" p10; trailing comma / capitals p22; missing full stops 4.1.8, 4.2.10, 9.4/10.1; redundant "(TMP)" re-definition p23; "2 week s" p44; missing word p44 |
| 1 Style variants | 8 | 7 | 88% | Prestart / pre-start |
| 2 Consistency | 23 | 22 | 96% | Stage 3 description p10 |
| 3 Template leftovers | 26 | 25 | 96% | 4.6.2 single bullet vs "no impact" p26 |
| 4 TGS and figures | 9 | 8 | 89% | Figure 2 caption and photo order p8 |
| **Total** | **110** | **97** | **88%** | 13 |

Pattern in misses: **missing full stops (3)** and small typos/spacing — the proofreading pass under-reports sentence-end punctuation. One figure (p8) was not checked by pass D (it reviews TGS pages, not body figures).

## Disagreements with the reference (likely false positives)
| Finding | TMP Check | Reference |
|---|---|---|
| p59 ×2 | Work trucks appear on/against the path | "Trucks shown on grass or in bays, clear of the path ✓" |
| p59 | +10% tolerance on a stated maximum cone spacing contradicts 7.3.2 | "4 m + 10% ✓" |
All three come from pass D (drawings). Vision placement judgements should be Query, not Moderate/Minor.

## Noise — why 211 findings for ~105 issues
| Source | Approx. findings | Fix |
|---|---|---|
| Same issue restated on each page it appears (e.g. duration conflict ×4, TC-N/A conflict ×4, complex wording ×6) | ~45 | Group by issue across pages (use `related_pages`); one finding lists all pages |
| Style/format nits beyond the reference (unit spacing, dash types, capitalisation, awkward wording) | 30 | Roll into one "Style sheet" finding per term, as the reference does |
| Repeated-sentence rule (Owner excluded this type in BENCH-01) | 3–5 | Downgrade to Query or drop `DUP-SENT` |
| Contents-entry nits split one per line | 3 | Merge with the contents finding |

Projected after fixes: **~120–130 findings, ~45–60 min review**, with recall unchanged.

## Valid extras worth noting (not in reference)
Accreditation number format differs cover vs TGS; review date later than Rev 0 date; declaration cites variations that don't exist; RTM / revision-register cells blank; risk at "1.2 m of moving traffic" contradicts no-lane-occupancy; "spotters at all times" vs spotters only for crane work; after-hours inspections vs no aftercare; no sign spacing dimensions on TGSs; pedestrian exclusion zone not shown; access to yacht club/boat ramp not addressed; 2020/21 data called "recent"; TGS 02 sign clipping. **To be confirmed by Tara.**

## Recommended actions
| # | Action | Owner | Cost |
|---|---|---|---|
| 1 | Cross-page issue grouping + style-sheet roll-up in the portal | AI-PM | $0 |
| 2 | Pass A prompt: explicit sentence-end punctuation and spacing checklist | AI-PM | $0 |
| 3 | Pass D: placement judgements → Query; add body figures (p7–8) | AI-PM | $0 |
| 4 | Re-run SU026 and re-score (BENCH-03) | Owner runs, AI-PM scores | ~US$3.50 |
| 5 | Tara validates the 31 substantive extras and 3 disagreements (blind rule: she has already set REF-01) | Tara via Owner | Reviewer time |

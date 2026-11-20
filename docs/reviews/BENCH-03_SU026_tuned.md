# BENCH-03 — Tuned engine (new prompts + AI issue grouping) vs REF-01

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Document | SU026 (61 pp), local portal on Owner's PC, check 6 (A-18) |
| Engine | `det_checks` 0.2 (DUP-SENT → Query) + passes A–D (BENCH-02 prompt changes) + AI grouping/style roll-up |
| Data | `customer-docs/wtgtm-2026-11-20/check-6-findings.json` (git-ignored) |
| Scorer | AI-PM — **simulated, not independent** (§5.3); Tara to confirm |
| Status | Under review |

## Results vs earlier runs
| Measure | BENCH-02 (raw) | BENCH-02b (grouped) | **BENCH-03** |
|---|---|---|---|
| Findings | 211 | 138 | **124** |
| Reference rows found | 97/110 (88%) | 98/110 (89%) | **97/110 (88%)** |
| Likely false positives | 3 | 2 | **0–1** (truck-on-path finding now rests mainly on a genuine text conflict: risk 3 vs risk 8 vs 7.1) |
| Est. review time (20–30 s/finding) | 70–105 min | 46–69 min | **41–62 min** (target 45) |
| AI cost | US$3.33 | US$3.51 | **US$2.75** |

## Recall by section
| Section | Rows | Found | Missed |
|---|---|---|---|
| Typos and grammar | 44 | 38 | Cert No. spacing; "upto"; "replaced on notice"; "erected" → "upright"; "St. John"; p44 missing word |
| Style variants | 8 | **8** | — |
| Consistency | 23 | 21 | Stage 3 description p10; pole setback |
| Template leftovers | 26 | 23 | 4.6.2 single bullet; p39 detour wording; "Implementation Standards" |
| TGS and figures | 9 | 7 | spotter not placed on plan; "Way2Go" company name |
| **Total** | **110** | **97 (88%)** | 13 |

**Fixed by BENCH-02 changes:** missing full stops (4.1.8, 4.2.10, 9.4/10.1), "2 week s", TMP re-definition, trailing comma, Prestart/pre-start, Figure 2 photo order (body figures now checked). Cone-spacing false positive gone.

**Run-to-run variation:** 7 items found in BENCH-02 were not found in BENCH-03 (e.g. "Way2Go", pole setback, detour wording) while 9 new ones were. The AI passes are not deterministic: on a single run, recall varies by about ±7 items around 88%. A single run should not be treated as complete; this supports the human-review gate (A-15) and the limitations wording.

## Grouping
The passes now report each conflict once with all pages (e.g. dates/duration across pp1, 6, 10, 44, 59–61; placeholders across pp25–33). Several reference items can sit in one finding, but each finding's suggested action names every location, so nothing is hidden. For the annotated PDF (D-12), each page in `pages` will carry its own mark.

## Conclusion
Engine is adequate for the G4 prototype on this document: recall ≈ 88%, ~0 false positives, review load ≈ target, cost ≈ A$4.20/check. Not yet evidence for G5 (one document, simulated scoring, run variance unmeasured beyond 2 runs).

## Next
| # | Action | Owner |
|---|---|---|
| 1 | Report PDF (D-11) and annotated PDF (D-12) — remaining G4 criteria | AI-PM |
| 2 | Tara confirms extras/disagreements and times a real review of check 6 | Tara via Owner |
| 3 | Benchmark ≥ 4 more WTGTM TMPs with reference findings (G2/G5) | Owner sources, AI-PM scores |

# TEST_REGISTER — TMP Check

Methodology: `docs/TEST_METHODOLOGY.md`. Test documents stored in `test-library/` (anonymised only) — live documents never committed.

## Test documents
| Doc ID | Set | Description | Pages | Reference findings by | Status |
|---|---|---|---|---|---|
| PUB-01 | T-EDGE (public) | MRWA TMP template, unfilled, DOCX→PDF | 42 | n/a (all placeholders expected) | Used in S-01 |
| T-SEED-01 | T-SEED | PUB-01 with 3 headings deleted, 1 renamed; TOC left stale | 42 | AI-PM (seeded ground truth: `T-SEED-01.expected.json`) | Used in TD-01 |
| REF-01 | T-HIST | Proofread report (~105 findings) for a 61-pp site-specific TMP; source TMP received 2026-11-20 (REF-01-SRC) | 4 (report) | Confirmed correct by WTGTM (A-19); transcribed to 110 scored rows (BENCH-02) | Used in D-02, D-03, B-02 to B-05 (portal line), L-06 |
| REF-01-SRC | T-HIST | Source TMP for REF-01 (redacted by customer), 61 pp incl. 3 TGSs | 61 | REF-01 (A-19) | Used in D-02, D-03, B-02 to B-05 (portal line), L-06 |
| — | T-HIST | Further WTGTM evidence | — | — | Awaiting input |

## Runs
| Run ID | Date | Engine ver | Rule-set ver | Docs | Recall | Precision | Unsupported Critical | Citation acc. | Review min | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| D-03 | 2026-11-20 | template_diff 0.1 + det_checks 0.2 + score 0.1 (LLM not run — key not loaded) | 22 core + patterns | REF-01 source TMP (61 pp) | 10/110 (9%) — A 1/52, B 0/23, C 9/26, D 0/9 | 18/18 (100%), 3 excluded | 0 | 100% | n/a | Full-reference scoring. See docs/reviews/BENCH-02 |
| B-05 | 2026-11-20 | portal engine, two runs (A-27) | 22 core + patterns | REF-01-SRC | 92% | 152 findings, 1 FP | 0 | — | — | US$4.86. docs/reviews/BENCH-05 (registered retrospectively 2026-11-25) |
| B-04 | 2026-11-20 | portal engine, repeat run | 22 core + patterns | REF-01-SRC | 84–88% single; 91% two-run union | — | 0 | — | — | docs/reviews/BENCH-04 |
| B-03 | 2026-11-20 | portal engine, tuned | 22 core + patterns | REF-01-SRC | 88% | 124 findings, ~0 FP | 0 | — | 41–62 est. | US$2.75. docs/reviews/BENCH-03 |
| B-02 | 2026-11-20 | portal engine + dedupe/grouping | 22 core + patterns | REF-01-SRC | 88% (97/110); 89% after grouping | 211 → 138 findings, 3 likely FP | 0 | — | — | US$3.33. docs/reviews/BENCH-02_SU026_AI_passes |
| L-06 | 2026-11-25 | llm_checks untuned (claude-opus-5-5, effort high, A–D ×1) + det_checks 0.2 | 22 core + patterns | REF-01 source TMP (61 pp) | 95/110 (86%); A 41/52, B 22/23, C 24/26, D 8/9 | Not yet measured — ~55 additional findings to adjudicate | 0 | n/a (no category E) | n/a | US$2.62, 13 min. AI-PM adjudication (simulated). See docs/reviews/BENCH-06 |
| D-02 | 2026-11-20 | template_diff 0.1 + det_checks 0.2 | 22 core + patterns | REF-01 source TMP (61 pp) | 9/26 leftovers (35%) | 18/21 confirmed (86%), 3 to adjudicate | 0 | 100% | n/a | No LLM. See docs/reviews/BENCH-01 |
| TD-01 | 2026-11-20 | template_diff 0.1 | WA-COP-4.2.1-001 | PUB-01 (control), T-SEED-01 | 3/3 (100%) | 3/3 (100%); control 0 FP of 109 | 0 | 100% (rule cited on every finding) | n/a | Rename tolerated; stale TOC correctly ignored |
| S-01 | 2026-11-20 | spike-0.1 | patterns only | PUB-01 | Not measured (no reference set) | 32/32 on inspected pages | 0 | n/a | n/a | See docs/reviews/SPIKE-S01_results.md |

## Defects
| Def ID | Run | Doc | Category | Description | Severity | Root cause | Resolution | Re-test |
|---|---|---|---|---|---|---|---|---|
| DEF-L06-1 | L-06 | REF-01 | A | Style-variant findings (21) all downgraded to Query, because their multi-page variant list can't match one page | Moderate | Validator assumes one quote on one page | Fixed 2026-11-25: `postprocess.locate_variants` checks each variant on any page (test added); re-score in next benchmark | — |
| DEF-L06-2 | L-06 | REF-01 | All | Same issue raised by several passes (278 raw findings) | Moderate | No cross-pass merge in llm_checks | Open: postprocess D4 (branch g4-postprocess-fixes) | — |
| DEF-L06-3 | L-06 | REF-01 | A | 10 small punctuation/spacing misses | Minor | Below the LLM's attention | Partly fixed: 'No.X' covered by WF-NOSPACE. Missing full-stop rule open: needs REF-01 examples to keep false positives low | — |
| DEF-D02-1 | D-02 | REF-01 | A/B | TGS sheets flagged as missing header; title block flagged as duplicate | Minor | Drawing pages not distinguished | Landscape pages exempted | Pass |
| DEF-C14-1 | Check 14 | SU 025 | Output | 31 findings marked with a page-top note instead of a highlight; 29 of their quotes were in the document | Major | Highlighting used exact phrase search on the cited page only (ligatures, line breaks, quote on a related page) | Word-level locator shared with validation, NFKC ligature folding, related pages tried: 147/149 text findings highlighted on check 14 data | Pass |
| DEF-C14-2 | Checks 14, 15 | SU 025, SU 026 | All | A merged finding could carry a Major/Moderate severity with an unlocated quote as its evidence | Critical (§2) | `processing.merge` took the highest severity and longest evidence from all members | Severity and evidence taken from located members only; no located member → Query; VISUAL-only Critical → Query | Pass (unit tests) |
| DEF-C14-3 | Check 14 | SU 025 | Output | Rule findings issued with no suggested action | Minor | No action text on rules | `det_checks.ACTIONS` for every rule | Pass |
| DEF-C14-4 | Check 14 | SU 025 | Output | Rule evidence cut mid-word at 120 characters | Minor | Fixed-width slice | Word-boundary snippet with ellipsis | Pass |
| DEF-C14-5 | Check 14 | SU 025 | A | 'Sentence repeated 2 times (pages 38)'; TGS title blocks flagged as repeats | Minor | Wording; portrait TGS sheets not detected | 'twice on page 38' / 'pages 35 and 36'; title-block drawing detection (postprocess D5). SU 025 DUP-SENT 9 → 3 | Pass |
| DEF-C14-6 | Check 14 | SU 025 | Output | Category E in scope but no E result stated | Minor | Report omitted the category count | 'Findings by category' line; states when no E rule was triggered | Pass |
| DEF-S01-1 | S-01 | PUB-01 | C | Duplicate/mis-labelled findings | Major | Substring re-search | Word-level bboxes + merge | Pass |
| DEF-S01-2 | S-01 | PUB-01 | C | TOC leaders flagged as blanks | Major | Over-broad regex | Dots-only word rule | Pass |
| DEF-S01-3 | S-01 | PUB-01 | Output | Annotation colour clashes with template | Minor | Highlight colour | Red outline | Pass |

## PORTAL-S1 — 2026-11-20
| Test | Result |
|---|---|
| `tests/portal/test_portal.py` — ledger derivation (consume, reversal, expiry), tenant scoping, final-only completion count, savings baseline gate, prices vs A-02/A-03, no GST-inclusive label, no mock-up figures or forbidden words on 6 pages, 22 rules listed | 15/15 pass |
| Playwright render 1536/1024/390 px; horizontal overflow | 0 px all widths — `docs/reviews/screens/` |

## PORTAL-S4 — 2026-11-20
| Test | Result |
|---|---|
| `tests/portal/test_workflow.py`: full workflow (7/7 seeded issues found, credit consumed at draft, original byte-identical, edit needs note, final blocked until all decided), no-credit rejection, invalid type/empty/renamed/oversize rejected with no credit, corrupt PDF → failed with no credit, other organisation gets 404 on check/original/final | 8/8 pass (23/23 portal total) |
| Playwright browser run: upload sample → draft → accept 7 → Final issued | Pass — `docs/reviews/screens/check-draft.png` |

## OWNER-FT-01 — 2026-11-20 — Owner functional test on SU026 (local portal, Windows)
| Item | Result |
|---|---|
| Upload 61-page SU026 under A-26 limit | Pass |
| Rule-based checks only (AI passes not active in that session) | 21 findings: 0 Critical, 0 Major, 8 Moderate, 9 Minor, 4 Query |
| Owner accepted all findings → final issued | Workflow pass. Not a benchmark: decisions were test clicks, not Tara's review |
| Next | Re-run with AI passes; score against REF-01 (~105 items) as BENCH-02 |

## OWNER-FT-02 — 2026-11-20 — SU026 with AI passes A–D (Owner's PC)
| Item | Result |
|---|---|
| AI passes A,B,C,D + rule checks | 293 findings: 0 Critical, 12 Major, 73 Moderate, 188 Minor, 20 Query |
| Actual AI cost | **US$3.33** for a 61-page TMP (estimate was US$2–4) |
| Defect found | Same issue reported by several passes (e.g. p25 template leftover ×4) → duplicate merging added; AI 'fix' and category were not shown → fixed |
| Next | Owner runs `devtools dedupe 5`, exports JSON → BENCH-02 scoring vs REF-01 (~105 items) |

## BENCH-02 — 2026-11-20 — SU026, rules + AI passes A–D (simulated scoring)
| Measure | Result |
|---|---|
| Recall vs REF-01 | 97/110 rows (88%); leftovers 25/26, consistency 22/23, typos 35/44, TGS 8/9 |
| Likely false positives | 3 (all pass D drawing placement) |
| Findings | 211 (after merge) for ~105 issues — reviewer time 70–105 min, target 45 **not met** |
| Cost | US$3.33 |
| Detail | `docs/reviews/BENCH-02_SU026_AI_passes.md` |

## BENCH-02b — 2026-11-20 — grouping applied to check 5
| Measure | Result |
|---|---|
| Findings | 211 → 138; recall 98/110 (89%), no reference item lost |
| Over-merges | 3 (prompt tightened) |
| Review time est. | 46–69 min (target 45) |

## BENCH-03 — 2026-11-20 — SU026 tuned engine (simulated scoring)
| Measure | Result |
|---|---|
| Findings | 124; recall 97/110 (88%); false positives 0–1; review est. 41–62 min; US$2.75 |
| Run variance | ±7 reference items between runs |
| Detail | `docs/reviews/BENCH-03_SU026_tuned.md` |

## BENCH-04 — 2026-11-20 — repeat run (check 7) and run union
| Measure | Result |
|---|---|
| Check 7 alone | 92/110 (84%), 122 findings, 1 FP, US$2.58 |
| Check 6 + 7 union | 100/110 (91%) |
| Checks 5 + 6 + 7 union | 106/110 (96%) |
| Detail | `docs/reviews/BENCH-04_SU026_repeat_run.md` |

## BENCH-05 — 2026-11-20 — two-run default (check 8)
| Measure | Result |
|---|---|
| Recall | 101/110 (92%); 152 findings; 1 FP; review est. 51–76 min; US$4.86 |
| Detail | `docs/reviews/BENCH-05_SU026_two_run.md` |

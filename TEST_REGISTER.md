# TEST_REGISTER — TMP Check

Methodology: `docs/TEST_METHODOLOGY.md`. Test documents stored in `test-library/` (anonymised only) — live documents never committed.

## Test documents
| Doc ID | Set | Description | Pages | Reference findings by | Status |
|---|---|---|---|---|---|
| PUB-01 | T-EDGE (public) | MRWA TMP template, unfilled, DOCX→PDF | 42 | n/a (all placeholders expected) | Used in S-01 |
| T-SEED-01 | T-SEED | PUB-01 with 3 headings deleted, 1 renamed; TOC left stale | 42 | AI-PM (seeded ground truth: `T-SEED-01.expected.json`) | Used in TD-01 |
| REF-01 | T-HIST | Proofread report (~105 findings) for a 61-pp site-specific TMP; source TMP received 2026-11-20 (REF-01-SRC) | 4 (report) | Confirmed correct by WTGTM (A-19) | Awaiting input (source TMP) |
| REF-01-SRC | T-HIST | Source TMP for REF-01 (redacted by customer), 61 pp incl. 3 TGSs | 61 | REF-01 (A-19) | Used in D-02 |
| — | T-HIST | Further WTGTM evidence | — | — | Awaiting input |

## Runs
| Run ID | Date | Engine ver | Rule-set ver | Docs | Recall | Precision | Unsupported Critical | Citation acc. | Review min | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| D-02 | 2026-11-20 | template_diff 0.1 + det_checks 0.2 | 22 core + patterns | REF-01 source TMP (61 pp) | 9/26 leftovers (35%) | 18/21 confirmed (86%), 3 to adjudicate | 0 | 100% | n/a | No LLM. See docs/reviews/BENCH-01 |
| TD-01 | 2026-11-20 | template_diff 0.1 | WA-COP-4.2.1-001 | PUB-01 (control), T-SEED-01 | 3/3 (100%) | 3/3 (100%); control 0 FP of 109 | 0 | 100% (rule cited on every finding) | n/a | Rename tolerated; stale TOC correctly ignored |
| S-01 | 2026-11-20 | spike-0.1 | patterns only | PUB-01 | Not measured (no reference set) | 32/32 on inspected pages | 0 | n/a | n/a | See docs/reviews/SPIKE-S01_results.md |

## Defects
| Def ID | Run | Doc | Category | Description | Severity | Root cause | Resolution | Re-test |
|---|---|---|---|---|---|---|---|---|
| DEF-D02-1 | D-02 | REF-01 | A/B | TGS sheets flagged as missing header; title block flagged as duplicate | Minor | Drawing pages not distinguished | Landscape pages exempted | Pass |
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

# TEST_REGISTER — TMP Check

Methodology: `docs/TEST_METHODOLOGY.md`. Test documents stored in `test-library/` (anonymised only) — live documents never committed.

## Test documents
| Doc ID | Set | Description | Pages | Reference findings by | Status |
|---|---|---|---|---|---|
| PUB-01 | T-EDGE (public) | MRWA TMP template, unfilled, DOCX→PDF | 42 | n/a (all placeholders expected) | Used in S-01 |
| T-SEED-01 | T-SEED | PUB-01 with 3 headings deleted, 1 renamed; TOC left stale | 42 | AI-PM (seeded ground truth: `T-SEED-01.expected.json`) | Used in TD-01 |
| REF-01 | T-HIST | Proofread report (~105 findings) for a 61-pp site-specific TMP; source TMP received 2026-11-20 (REF-01-SRC) | 4 (report) | Confirmed correct by WTGTM (A-19); transcribed to 110 scored rows (BENCH-02) | Used in D-02, D-03 |
| REF-01-SRC | T-HIST | Source TMP for REF-01 (redacted by customer), 61 pp incl. 3 TGSs | 61 | REF-01 (A-19) | Used in D-02 |
| — | T-HIST | Further WTGTM evidence | — | — | Awaiting input |

## Runs
| Run ID | Date | Engine ver | Rule-set ver | Docs | Recall | Precision | Unsupported Critical | Citation acc. | Review min | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| D-03 | 2026-11-20 | template_diff 0.1 + det_checks 0.2 + score 0.1 (LLM not run — key not loaded) | 22 core + patterns | REF-01 source TMP (61 pp) | 10/110 (9%) — A 1/52, B 0/23, C 9/26, D 0/9 | 18/18 (100%), 3 excluded | 0 | 100% | n/a | Full-reference scoring. See docs/reviews/BENCH-02 |
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

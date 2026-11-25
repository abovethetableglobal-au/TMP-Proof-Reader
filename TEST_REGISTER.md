# TEST_REGISTER — TMP Check

Methodology: `docs/TEST_METHODOLOGY.md`. Test documents stored in `test-library/` (anonymised only) — live documents never committed.

## Test documents
| Doc ID | Set | Description | Pages | Reference findings by | Status |
|---|---|---|---|---|---|
| PUB-01 | T-EDGE (public) | MRWA TMP template, unfilled, DOCX→PDF | 42 | n/a (all placeholders expected) | Used in S-01 |
| T-SEED-01 | T-SEED | PUB-01 with 3 headings deleted, 1 renamed; TOC left stale | 42 | AI-PM (seeded ground truth: `T-SEED-01.expected.json`) | Used in TD-01 |
| REF-01 | T-HIST | Proofread report (~105 findings) for a 61-pp site-specific TMP; source TMP received 2026-11-20 (REF-01-SRC) | 4 (report) | Confirmed correct by WTGTM (A-19) | Used in D-02, L-01 |
| REF-01-SRC | T-HIST | Source TMP for REF-01 (redacted by customer), 61 pp incl. 3 TGSs | 61 | REF-01 (A-19) | Used in D-02, L-01 |
| — | T-HIST | Further WTGTM evidence | — | — | Awaiting input |

## Runs
| Run ID | Date | Engine ver | Rule-set ver | Docs | Recall | Precision | Unsupported Critical | Citation acc. | Review min | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| L-01 | 2026-11-25 | llm_checks (claude-opus-5-5, effort high, A–D ×1) + det_checks 0.2 | 22 core + patterns | REF-01 source TMP (61 pp) | 95/110 (86%); A 41/52, B 22/23, C 24/26, D 8/9 | Not yet measured — ~55 additional findings to adjudicate | 0 | n/a (no category E) | n/a | US$2.62, 13 min. AI-PM adjudication (simulated). See docs/reviews/BENCH-03 |
| D-02 | 2026-11-20 | template_diff 0.1 + det_checks 0.2 | 22 core + patterns | REF-01 source TMP (61 pp) | 9/26 leftovers (35%) | 18/21 confirmed (86%), 3 to adjudicate | 0 | 100% | n/a | No LLM. See docs/reviews/BENCH-01 |
| TD-01 | 2026-11-20 | template_diff 0.1 | WA-COP-4.2.1-001 | PUB-01 (control), T-SEED-01 | 3/3 (100%) | 3/3 (100%); control 0 FP of 109 | 0 | 100% (rule cited on every finding) | n/a | Rename tolerated; stale TOC correctly ignored |
| S-01 | 2026-11-20 | spike-0.1 | patterns only | PUB-01 | Not measured (no reference set) | 32/32 on inspected pages | 0 | n/a | n/a | See docs/reviews/SPIKE-S01_results.md |

## Defects
| Def ID | Run | Doc | Category | Description | Severity | Root cause | Resolution | Re-test |
|---|---|---|---|---|---|---|---|---|
| DEF-D03-1 | L-01 | REF-01 | A | Style-variant findings (21) all downgraded to Query, because their multi-page variant list can't match one page | Moderate | Validator assumes one quote on one page | Open: validate per variant | — |
| DEF-D03-2 | L-01 | REF-01 | All | Same issue raised by several passes (278 raw findings) | Moderate | No cross-pass merge in llm_checks | Open: postprocess D4 (branch g4-postprocess-fixes) | — |
| DEF-D03-3 | L-01 | REF-01 | A | 10 small punctuation/spacing misses | Minor | Below the LLM's attention | Open: deterministic end-of-paragraph full-stop and 'No.X' rules | — |
| DEF-D02-1 | D-02 | REF-01 | A/B | TGS sheets flagged as missing header; title block flagged as duplicate | Minor | Drawing pages not distinguished | Landscape pages exempted | Pass |
| DEF-S01-1 | S-01 | PUB-01 | C | Duplicate/mis-labelled findings | Major | Substring re-search | Word-level bboxes + merge | Pass |
| DEF-S01-2 | S-01 | PUB-01 | C | TOC leaders flagged as blanks | Major | Over-broad regex | Dots-only word rule | Pass |
| DEF-S01-3 | S-01 | PUB-01 | Output | Annotation colour clashes with template | Minor | Highlight colour | Red outline | Pass |

# TEST_REGISTER — TMP Check

Methodology: `docs/TEST_METHODOLOGY.md`. Test documents stored in `test-library/` (anonymised only) — live documents never committed.

## Test documents
| Doc ID | Set | Description | Pages | Reference findings by | Status |
|---|---|---|---|---|---|
| PUB-01 | T-EDGE (public) | MRWA TMP template, unfilled, DOCX→PDF | 42 | n/a (all placeholders expected) | Used in S-01 |
| — | T-HIST | Awaiting WTGTM evidence | — | — | Awaiting input |

## Runs
| Run ID | Date | Engine ver | Rule-set ver | Docs | Recall | Precision | Unsupported Critical | Citation acc. | Review min | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| S-01 | 2026-11-20 | spike-0.1 | patterns only | PUB-01 | Not measured (no reference set) | 32/32 on inspected pages | 0 | n/a | n/a | See docs/reviews/SPIKE-S01_results.md |

## Defects
| Def ID | Run | Doc | Category | Description | Severity | Root cause | Resolution | Re-test |
|---|---|---|---|---|---|---|---|---|
| DEF-S01-1 | S-01 | PUB-01 | C | Duplicate/mis-labelled findings | Major | Substring re-search | Word-level bboxes + merge | Pass |
| DEF-S01-2 | S-01 | PUB-01 | C | TOC leaders flagged as blanks | Major | Over-broad regex | Dots-only word rule | Pass |
| DEF-S01-3 | S-01 | PUB-01 | Output | Annotation colour clashes with template | Minor | Highlight colour | Red outline | Pass |

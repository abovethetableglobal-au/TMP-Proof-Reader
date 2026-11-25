# BENCH-02 — SU026 scored against the full REF-01 reference (110 rows)

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Document | REF-01-SRC (61 pp, redacted), git-ignored `customer-docs/wtgtm-2026-11-20/` |
| Reference | REF-01 (A-19), transcribed to `customer-docs/wtgtm-2026-11-20/REF-01.expected.json` (git-ignored, customer-derived) |
| Scorer | `src/tmpcheck/score.py` v0.1 — auto-match proposals (page ±1 + keyword overlap) + manual adjudication file |
| Status | **Blocked (partial)** — LLM passes not run: `ANTHROPIC_API_KEY` not loaded in this container |

## Reference set
REF-01's own summary gives 41 + 8 + 23 + 24 + 9 = **105**. Transcribed row by row it has **110 issue rows** (44 typo rows + 8 style variants, 23 consistency, 26 leftover rows, 9 TGS issues). 7 "checked ✓" rows (2 consistency, 5 TGS) are not issues and are not scored. Scoring uses the 110 rows.

| Cat | Name | Rows |
|---|---|---|
| A | Typos, grammar, style | 52 |
| B | Consistency | 23 |
| C | Template leftovers / completeness | 26 |
| D | TGS and figures | 9 |

## Results — deterministic engine only (template_diff 0.1 + det_checks 0.2)
| Measure | Result |
|---|---|
| Recall vs 110 rows | **10/110 (9%)** — A 1/52, B 0/23, C 9/26, D 0/9 |
| Findings raised | 21: 17 matched, 1 valid not in reference (p10 TBA), 3 excluded by Owner (repeated sentences) |
| Precision (scored) | 18/18 (100%) |
| Template headings | 109/109 matched |
| Cost | $0 |

Agrees with BENCH-01 (9/26 leftovers); the additional hit is the cover TBA date (T01).

## LLM passes — not run
| Step | Result |
|---|---|
| 1. Key loads | **Fail** — variable is defined on the environment but absent from this container (variables load only at container start) |
| 4. `llm_checks` run | Dry-run only: 4 requests built (3.6 MB PDF). No API call made, no cost incurred |
| 5. Score LLM findings | Not done — scorer and reference ready |
| 6. Actual cost | Not measured |

## Scorer self-test
Synthetic LLM-format file (no customer data): 2 planted matches found, 1 unrelated finding left "to adjudicate". Pass.

## Next run (new session with key loaded)
```
python3 -m src.tmpcheck.llm_checks customer-docs/wtgtm-2026-11-20/SU026_redacted.pdf customer-docs/wtgtm-2026-11-20/out/llm.json
python3 -m src.tmpcheck.score customer-docs/wtgtm-2026-11-20/REF-01.expected.json customer-docs/wtgtm-2026-11-20/out/det.json customer-docs/wtgtm-2026-11-20/out/llm.json --adj customer-docs/wtgtm-2026-11-20/out/adj_det.json --out customer-docs/wtgtm-2026-11-20/out/score_all.json
```
Then adjudicate every "to adjudicate" finding (valid-not-in-reference vs false positive) and spot-check auto matches before recording recall/precision. Auto-matches are proposals, not verdicts.

Note: `customer-docs/` is git-ignored — the reference JSON, adjudication file and outputs must be recreated (or re-uploaded) in each new container.

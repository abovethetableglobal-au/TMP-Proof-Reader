# BENCH-01 — Deterministic checks vs reference findings (REF-01)

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Document | REF-01 source TMP (61 pp incl. 3 TGSs, redacted by customer), stored in git-ignored `customer-docs/` |
| Reference | REF-01 proofread report, confirmed correct by WTGTM (A-19) |
| Engine | `template_diff` 0.1 + `det_checks` 0.2 — deterministic only, **no LLM, $0** |
| Scope scored | Reference section 3 "Template leftovers and placeholders" (26 rows) |
| Status | Quality checked |

## Results
| Measure | Result |
|---|---|
| Template headings (109) | 109 matched, 0 missing — agrees with reference (no missing sections reported) |
| Reference leftovers detected | **9 of 26 (35%)** |
| TMP Check findings raised | 21 |
| Confirmed correct | 18 (incl. 1 valid issue not in the reference: same garbled 'TBA' date on p10 as on the cover) |
| Confirmed false positives | 0 (after DEF-D02-1 fix; 4 before) |
| Excluded by Owner (2026-11-20) | 3 repeated sentences not listed in the reference — ignore |
| Precision | 100% on scored findings (18/18); 3 excluded |
| Run time | < 1 s |

## Detected (9)
Sub-contractor 'TBA' · two `<…>` placeholders in consultation section · two `<…>` placeholders in roles section · Main Roads / complex-arrangement / RIM wording in an LGA-road TMP · `<…>` header placeholder in TGS table · repeated cone-inspection sentence · blank start/finish dates in appendix · Queensland agency (TMR) in incident form · inserted pages without header (page-number drift)

## Not detected (17) — need semantic understanding (LLM) or table/vision parsing
| Type | Count | Planned method |
|---|---|---|
| Contradictions between sections (e.g. 'no impact' vs listed impacts; N/A sections described as applicable) | 6 | LLM consistency pass with fact sheet |
| Blank table cells / empty registers / missing evidence pages | 4 | Table extraction + rules |
| Duplicated paragraphs with small wording changes, misplaced text | 3 | Fuzzy similarity (threshold tuning) |
| Wrong/unlabelled table and section cross-references, missing footnotes | 2 | Cross-reference resolver |
| Documents referenced that don't exist; contact-list completeness | 2 | Rules + LLM |

## Defects
| ID | Defect | Fix |
|---|---|---|
| DEF-D02-1 | TGS drawing sheets flagged as 'missing header' (3) and repeating title block flagged as duplicate sentence (1) | Landscape drawing pages exempted from header and duplicate checks |

## Conclusions
1. **Verified:** deterministic checks find about a third of template leftovers with no false positives, at zero cost — keep them as the first pass.
2. **Source-supported conclusion:** most of the reference value (typos, consistency, contradictions, TGS checks — ~95 of ~105 items) requires the LLM pass. G4 cannot be met without the API key.
3. **Recommendation:** next build the LLM pass for categories A and B, then score the full REF-01 (all ~105 items).

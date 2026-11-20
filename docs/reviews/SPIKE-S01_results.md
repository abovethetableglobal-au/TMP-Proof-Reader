# SPIKE S-01 — Extraction, completeness checks & annotation (public template)

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Input | PUB-01 MRWA TMP template (unfilled), DOCX → PDF via LibreOffice, 42 pages |
| Code | `src/spike/completeness_spike.py` (deterministic; no LLM; no customer data; $0) |
| Status | Quality checked (spike scope only) |

## Results (final run)
| Measure | Result | Evidence class |
|---|---|---|
| Pages extracted | 42/42 | Verified fact |
| Findings | 32 (31 Moderate, 1 Minor) — placeholders, blank dates, `[insert …]` instructions | Verified fact |
| False positives on visual check (p1, p6) | 0 after fixes | Verified fact (2 pages inspected) |
| Every finding's evidence locatable on cited page | Yes (asserted in code) | Verified fact |
| Original file unchanged (SHA-256 before/after) | Yes | Verified fact |
| Annotated copy produced, IDs linked to report | Yes | Verified fact |
| Processing time | 0.15 s | Verified fact |

## Defects found & fixed
| ID | Defect | Fix |
|---|---|---|
| DEF-S01-1 | Substring re-search duplicated findings ("XX" inside "XXXXX"), dropped date findings — 150 raw findings | Word-level bboxes; adjacent placeholders merged per field |
| DEF-S01-2 | Table-of-contents dot leaders flagged as blank fields (~97 false positives) | Dots rule applies only to words consisting solely of dots |
| DEF-S01-3 | Template's own yellow highlighting indistinguishable from TMP Check marks | Red outline annotations |

## Known misses (open)
| ID | Miss | Proposed approach |
|---|---|---|
| GAP-S01-1 | Template heading placeholders ("WORK TYPE", "Road Number, Road Name, Suburb, SLK") | **Template-diff check:** compare submission against the blank template it came from (needs WTGTM templates, item A5) |
| GAP-S01-2 | Single-character placeholder ("Rev. No. X"), short dots ("Contract …….") | Field-aware rules keyed to template labels |
| GAP-S01-3 | Header "OFFICIAL" wrapped as "OFFICI / AL" — LibreOffice rendering artefact | Prefer customer-supplied PDFs; record DOCX conversion as a known limitation |

## Conclusions
1. **Source-supported conclusion:** Extraction, evidence-bound findings and non-destructive annotation are feasible at negligible cost with open-source tooling.
2. **Recommendation:** Build category C completeness primarily as a *template-diff* against WTGTM's own templates, with pattern rules as a backstop. This raises the priority of evidence item A4 (renumbered in request v0.2).
3. **Hypothesis (untested):** Most category A–C value can be delivered deterministically, reserving LLM cost for proofreading nuance and categories D–E — to be tested in G4.

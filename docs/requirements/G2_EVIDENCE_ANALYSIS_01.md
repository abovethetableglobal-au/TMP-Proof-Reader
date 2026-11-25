# G2 Evidence Analysis 01 — Reference proofread report (REF-01)

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Evidence | Proofread report (4 pp) on a 61-page site-specific TMP incl. 3 TGSs; LGA-road car-park works; reviewed 18/11/2026 |
| Stored | `customer-docs/wtgtm-2026-11-20/` (git-ignored). This analysis contains no personal or project-identifying details. |
| Request items satisfied | A3 (proofreader corrections) for 1 TMP only. **Not received:** the TMP itself (A1), its TGSs (A2), templates (A4), A5–A9, Section B answers |
| Status | Ready for user review |

## 1. Provenance — **resolved 2026-11-20:** confirmed correct by WTGTM (A-19); customer name is 'Way to Go' (A-20)
- PDF metadata: author = the Owner's business; generator = ReportLab (a code-generated PDF). **Assumption to check:** it may have been produced by an AI tool rather than the historical external proofreader.
- If AI-produced, it is **not** independent ground truth. Tara must validate it (TEST_METHODOLOGY §1) before it is used to score TMP Check.
- The report recommends changing a title-block company name to "Way to Go"; the project brief names the customer "Way Too Go". One of these is wrong — confirm the legal/trading name.

## 2. What a good check looks like (benchmark scale)
| Pass | Findings | Maps to category |
|---|---|---|
| Typos & grammar | 41 + 8 style variants | A |
| Consistency | 23 (2 confirmed-correct checks also reported) | B |
| Template leftovers & placeholders | 24 | C |
| TGS & figures | 9 issues + 5 checks passed | D |
| Compliance | 0 (no compliance section) | E — gap TMP Check adds |
| **Total** | **~105 items on 61 pages** | |

**Source-supported conclusion:** the customer value bar is ~100 actionable items per 60-page TMP, presented as page/section/found/fix tables plus open questions for the designer.

## 3. New engine requirements derived
| ID | Requirement | Category | Method | Status |
|---|---|---|---|---|
| RQ-01 | Detect `<…>` angle-bracket template instructions | C | Pattern (extend S-01) | New |
| RQ-02 | Contents page vs actual headings and page numbers (titles and page refs) | B/C | Deterministic | New |
| RQ-03 | Recalculate risk scores (Likelihood × Consequence) and rating bands; check against the TMP's own matrix | B/E | Deterministic table parse | New |
| RQ-04 | Internal cross-references point to the right section (e.g. "see 7.3.2") | B | Deterministic + LLM | New |
| RQ-05 | Jurisdiction-wrong wording: Main Roads / 'complex arrangement' / RIM language left in LGA-road TMPs; wrong-state text | C/E | Rule + LLM | New |
| RQ-06 | Duplicated or misplaced paragraphs (text pasted under the wrong heading) | A/C | Similarity | New |
| RQ-07 | Date logic: TGS dates vs site-inspection date vs TMP date; programme dates and durations consistent across cover, body, appendices, TGS title blocks | B | Fact extraction | New |
| RQ-08 | Numeric fact consistency (vehicle counts, traffic volumes, speeds, setbacks, device sizes) across the document | B | Fact extraction + LLM | New |
| RQ-09 | Contact and role consistency (names, emails, role titles); people appearing only once | B | Fact extraction | New |
| RQ-10 | Acronym list complete and correct vs acronyms used | A/C | Deterministic | New |
| RQ-11 | Emergency contacts table completeness (LGA, supervisor, WorkSafe, Police non-emergency) | C | Checklist rule (needs Tara confirmation) | New |
| RQ-12 | TGS title block (date, revision, duration, company name, sign quantities) vs TMP text | D | Vision + text | New |
| RQ-13 | Drawing defects: text or signs clipped by the drawing frame; items described in text but not placed on the plan (e.g. spotter) | D | Vision (LLM) | New |
| RQ-14 | Printed page numbers vs PDF page numbers; report both where they differ | Output | Deterministic | New |
| RQ-15 | Australian English spelling and style consistency list (variant spellings of the same term) | A | Dictionary + LLM | New |
| RQ-16 | "Open questions for the designer" section in the report where facts conflict and cannot be resolved | Output | Report template | New |
| RQ-17 | Risk ratings correct per the TMP's §3.2 risk matrix: every Likelihood × Consequence pair maps to the matrix's rating (initial and residual). Extends RQ-03 | B/E | Deterministic table parse | New — Tara 2026-11-25 |
| RQ-18 | Risk register 'TMP section' reference matches the hazard topic (e.g. rail crossing → §4.2.8). Extends RQ-04 | B | Hazard→section map (template) + LLM | New — Tara 2026-11-25 |

## 4. Output format implications
The reference report's structure (method table → findings by pass with Page / Section / Found / Fix → summary counts → open questions) is clear and practical. **Recommendation:** adopt it as the base layout for Output 1, adding Severity, Finding ID (linked to annotations) and Source reference columns required by Handover §6.

## 5. Next evidence needed
1. The 61-page TMP (incl. TGSs) that this report reviewed — needed to benchmark TMP Check against these ~105 findings.
2. Remaining items A1–A9 and Section B answers.

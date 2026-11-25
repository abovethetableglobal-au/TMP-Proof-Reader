# BENCH-06 — LLM passes A–D + deterministic checks vs REF-01 (110 rows)

| Field | Value |
|---|---|
| Date | 2026-11-25 |
| Document | REF-01-SRC (61 pp incl. 3 TGSs, redacted), git-ignored `customer-docs/wtgtm-2026-11-20/` |
| Reference | REF-01 (A-19), 110 issue rows (same transcription as BENCH-02 partial, branch `claude/sleepy-gauss-4kbv9t`): A 52 (44 typo + 8 style), B 23, C 26, D 9 |
| Engine | `llm_checks` (claude-opus-5-5, effort high, 1 run of passes A–D) + `det_checks` 0.2 |
| Scoring | Manual adjudication by AI-PM — **simulated review** (§5.3), not independent. Adjudication file: `customer-docs/.../out/bench02_scoring.json` (git-ignored) |
| Status | Quality checked (AI-PM); awaiting Owner/WTGTM adjudication of additional findings |
| Note | Numbered BENCH-06: BENCH-02 to 05 already exist on the portal branch `claude/fervent-hopper-q3h87z` (tuned engine: 84–88% single run, 92% two-run). This run uses the **untuned** `llm_checks` on this branch and agrees with BENCH-04 single-run variance. |

## Recall vs REF-01
| Cat | Rows | Hit | Partial | Miss | Recall (hits) |
|---|---|---|---|---|---|
| A Typos/grammar | 44 | 33 | 1 | 10 | 75% |
| A Style variants | 8 | 8 | 0 | 0 | 100% |
| B Consistency | 23 | 22 | 0 | 1 | 96% |
| C Leftovers | 26 | 24 | 1 | 1 | 92% |
| D TGS/figures | 9 | 8 | 0 | 1 | 89% |
| **Total** | **110** | **95** | **2** | **13** | **86%** (88% incl. partials) |

Deterministic engine alone: 10/110 (9%, BENCH-02). It found no reference item the LLM missed, but it is still the zero-cost first pass and gives exact placeholder locations.

**Missed (13):** 10 small punctuation/wording items (missing full stops in 4.1.8, 4.2.10, 9.4 and 10.1; "Cert No.KTS"; "Site Constraint /Impacts" heading; "this Traffic Management Plan (TMP)" redefined; "replaced on notice"; "St. John"; "2 week s"; "Worker symbolic pedestrian management"), the PM contact email/Luka Broz conflict, the 8.1.1 detour wording, and the Figure 2 caption/photo order.

**Reference "✓ consistent" checks:** no finding contradicts the hours, the risk-register L×C scores, Figure 1, the sign quantities, or Note 5. **One disputed item:** B027/D013 say "4 m + 10%" on a maximum spacing contradicts 7.3.2, but REF-01 marks Note 2 as consistent. Owner/WTGTM to adjudicate.

## Output
| Measure | A | B | C | D | Total |
|---|---|---|---|---|---|
| Findings | 133 | 41 | 68 | 36 | 278 (raw, before de-duplication) |
| Evidence verified on page | 109 | 41 | 66 | 28 | 244 |
| VISUAL (reviewer to confirm) | 2 | 0 | 1 | 8 | 11 |
| Quote not found → Query | 22 | 0 | 1 | 0 | 23 |
| Critical findings | 0 | 0 | 0 | 0 | 0 (no unsupported Critical) |

**Additional findings not in REF-01:** about 55 distinct issues once cross-pass duplicates are removed. Examples: designer declaration "subject to the variations approved" vs no departures (B004/C002); three 4-week stages can't fit Nov–Dec 2026 (D002); no dimensions on any TGS (D015); trench/flagging areas not shown on the TGS (D016); no exclusion zone around the Hiab (D017). **Precision is not yet measured.** These must be adjudicated (valid / false positive) before a precision figure is recorded. Likely low-value items: "judgment" spelling (A055), "@4m" (A044).

## Cost and time (actual, measured)
| Pass | Output tokens | Cache | USD | Seconds |
|---|---|---|---|---|
| A | 33,052 | write 132,236 | 1.32 | 258 |
| B | 20,898 | read 132,236 | 0.45 | 176 |
| C | 26,474 | read 132,236 | 0.56 | 229 |
| D | 13,497 | read 132,236 | 0.30 | 121 |
| **Total** | 93,921 | — | **2.62** | 784 (~13 min, sequential) |

Verified fact: one run of A–D on a 61-page TMP costs US$2.62. The portal's "×2" runs cost $5–6 (check 14: $6.10 for 64 pp).

## Defects
| ID | Defect | Fix |
|---|---|---|
| DEF-L06-1 | All 21 style-variant findings (e.g. "car park / carpark / CarPark") are downgraded to Query, because their evidence lists variants from many pages and can't match one page | Validate each variant separately on any page, or exempt variant lists and label them "style" |
| DEF-L06-2 | Passes overlap heavily (e.g. the vehicle count conflict is raised by A026, B005, C009 and D030), inflating the counts | De-duplicate across passes: `postprocess.py` D4 on branch `g4-postprocess-fixes` |
| DEF-L06-3 | 10 small punctuation misses (missing full stops, spacing) | Add deterministic checks for a paragraph ending without a full stop and "No.X" spacing |

## Conclusions
1. **Verified:** the LLM passes lift recall from 9% (deterministic only) to 86% of REF-01 at US$2.62 per check, with no unsupported Critical.
2. **Source-supported conclusion:** these results are measured against the provisional pilot-entry targets in TEST_METHODOLOGY (A–C ≥ 90%, D ≥ 75%). D (89%), B (96%) and C (92%) meet them. A does not: 41/52 = 79%. The A misses are mostly mechanical punctuation, which rules catch more cheaply than extra LLM effort. A single benchmark on one document, adjudicated by the AI-PM rather than blind by Tara, is not evidence for the pilot-entry gate.
3. **Recommendation:** adjudicate the ~55 additional findings with WTGTM (precision); fix DEF-L06-1 to DEF-L06-3; re-run once to measure variance between runs.

# Checking Engine Test Methodology (v0.1)

## 1. Reference test library (Phase 2)
| Set | Content | Source | Purpose |
|---|---|---|---|
| T-HIST | Historical WTGTM TMPs + proofreader corrections | WTGTM (A1–A4) | Real-world recall vs human proofreader |
| T-SEED | Clean TMPs with **deliberately seeded** errors (spelling, consistency, missing info, TMP↔TGS mismatch, wrong clause) | Built by AI-PM from clean docs; seeds logged | Known ground truth per category |
| T-CLEAN | Correct documents / sections | Final corrected versions (A4), reviewer-confirmed | False-positive rate |
| T-REJ | Authority-rejected TMPs | WTGTM (A7) | High-value miss detection |
| T-EDGE | Scanned, rotated, DOCX-only, >80 pages, drawings-only | Constructed | Intake robustness & pre-credit rejection |

Ground truth for T-HIST, T-CLEAN and T-REJ is established by the **qualified reviewer**, independently of TMP Check output (blind).

## 2. Matching rules
A TMP Check finding **matches** a reference finding when: same issue, same page (±1), and category correct. Severity mismatches are recorded separately.

## 3. Metrics (per category A–E and overall)
| Metric | Definition | Pilot-entry target |
|---|---|---|
| Recall | matched ÷ reference findings | A–C ≥ 90%; D–E ≥ 75% (provisional) |
| Precision | matched ÷ TMP Check findings | ≥ 80% |
| Critical/Major recall | on reference Critical+Major | ≥ 95% (with human review) |
| Unsupported Critical | Critical without valid evidence | **0** |
| Citation accuracy | compliance findings with correct source+edition+clause | **100%** |
| Annotation accuracy | annotation on correct location | ≥ 95% |
| Intake rejection accuracy | unreadable/unsupported files caught pre-credit | 100% |
| Processing time | upload → draft report | record |
| Review time | reviewer minutes per check | record; target ≤ 45 min |
| Cost per check | AI + infra | record |

Targets are provisional and require Owner approval at G5.

## 4. Procedure
1. Freeze engine version + rule-set version for each run.
2. Run full library; store raw outputs.
3. Score automatically against reference JSON; reviewer adjudicates disputed matches.
4. Log to TEST_REGISTER: per-doc results, defects, root cause, fix, re-test.
5. Regression: every engine/rule change re-runs the full library before release.

## 5. Limitations
A finite test set cannot prove the absence of misses. Post-launch defect logging continues.

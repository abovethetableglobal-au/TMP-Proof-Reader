# BENCH-05 — Two-run default (A-27) vs REF-01

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Document | SU026, check 8 — passes A–D ×2, combined + grouped, new word-form rules |
| Data | `customer-docs/wtgtm-2026-11-20/check-8-findings.json` (git-ignored) |
| Scorer | AI-PM — **simulated, not independent** (§5.3) |
| Status | Under review |

## Results
| Measure | Check 6 (1 run) | Check 7 (1 run) | **Check 8 (2 runs)** |
|---|---|---|---|
| Findings | 124 | 122 | **152** |
| Reference rows found | 97/110 (88%) | 92/110 (84%) | **101/110 (92%)** |
| Likely false positives | 0–1 | 1 | 1 (cone spacing +10%, contradicts REF-01 "✓") |
| Est. review time (20–30 s/finding) | 41–62 min | 41–61 min | **51–76 min** (target 45) |
| AI cost | US$2.75 | US$2.58 | **US$4.86** (prompt caching kept the 2nd run cheaper than estimated) |

By section: typos 39/44, style 7/8, consistency 22/23, leftovers 25/26, TGS 8/9.

**New rules worked:** "upto" (WF-JOINED) and "Cert No.KTS" (WF-NOSPACE) found for the first time by any run.
**Still missed:** "ditch witch" capitalisation; "Advanced" warning signs; TMP re-definition; "erected"→"upright"; p44 missing word; TGS-1 style; Stage 3 description; p39 detour wording; spotter not placed on plan.

## Residual duplication
Two runs phrase the same problem differently, and grouping did not merge all of them. Examples: stage numbering (2 findings), Appendix E (2), speed limits (2), risk 5 conflicts (3), rain text (3), AGTTM tables (2). Estimated ~15 further merges possible → ~135 findings, ~45–68 min.

## Conclusion
Recall target (≥ 91%) met. False positives ≈ 1. Review load is 10–30 min above target and is now the main constraint. **Engine is adequate for the G4 prototype**; further tuning should be driven by Tara's measured review time on a real draft rather than more AI-PM-scored reruns.

# BENCH-04 — Repeat run of the tuned engine (variance and two-run union)

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Document | SU026, check 7 (same engine and settings as BENCH-03 / check 6) |
| Data | `customer-docs/wtgtm-2026-11-20/check-7-findings.json` (git-ignored) |
| Scorer | AI-PM — **simulated, not independent** (§5.3) |
| Status | Under review |

## Check 7 vs check 6 (same engine, same document)
| Measure | Check 6 (BENCH-03) | Check 7 |
|---|---|---|
| Findings | 124 | 122 |
| Reference rows found | 97/110 (88%) | **92/110 (84%)** |
| Likely false positives | 0–1 | 1 (cone spacing +10% — contradicts REF-01 "✓") |
| AI cost | US$2.75 | US$2.58 |

By section (check 7): typos 36/44, style 6/8, consistency 21/23, leftovers 22/26, TGS 7/9.
Check 7 newly found vs check 6: pole setback, "St. John", "Implementation Standards". Lost vs check 6: "There is another", template asterisk note, Prestart, TGS-1 style, TMP re-definition, "TMP will be communicated", "works nature", stage closure conflict.

## Union of runs (simulates "run twice and combine" — option A)
| Runs combined | Reference rows found | Still missed |
|---|---|---|
| Check 6 alone | 97/110 (88%) | 13 |
| Check 6 + 7 | **100/110 (91%)** | Cert No. spacing; "upto"; "replaced on notice"; "erected"→"upright"; p44 missing word; Stage 3 description; 4.6.2 bullet; p39 detour; spotter on plan; "Way2Go" |
| Checks 5 + 6 + 7 (check 5 = older prompts) | **106/110 (96%)** | "upto"; p44 missing word; Stage 3 description; 4.6.2 bullet |

## Findings
1. **Single-run recall on this document is 84–88%** with the current engine (two runs). R-25 confirmed.
2. **Two runs combined → 91%; three runs → ~96%.** Each extra run adds a few genuinely new items; most items are found by every run.
3. Items missed by every run are small typos ("upto", a missing word) and two subtle descriptive conflicts — candidates for a targeted deterministic check ("upto", run-together words) rather than more AI runs.
4. Combined runs will add findings before grouping; grouping should absorb most of the overlap. Expected ~135–150 findings → ~45–75 min review. To be measured.

## Recommendation
| Option | Recall (est.) | Cost/check | Review |
|---|---|---|---|
| 1 run (current) | 84–88% | ~US$2.70 | 40–60 min |
| **2 runs + grouping** | ~91% | ~US$5.40 | ~45–75 min |
| 3 runs + grouping | ~95% | ~US$8.10 | longer |
Recommend **2 runs + grouping** as default, plus a deterministic "run-together words" check ("upto", "alot", "week s"). At A$8/check against a $149 credit the cost is acceptable; review time is the constraint to watch.

# Check 11 (Owner PC) — TMP BC 016: output review v0.1

Review type: simulated (AI-PM only). Inputs: findings.json, report PDF (20 pp), annotated PDF (81 pp). Live TMP under A-41.
Run on branch claude/determined-curie-a43sdd (queue + Stripe build), AI passes A–D ×2.

| Metric | Check 11 (this run) | Check 19 (previous) |
|---|---|---|
| Findings | 182: 0 Critical, 16 Major, 51 Moderate, 87 Minor, 28 Query | 192: 0 / 17 / 42 / 102 / 31 |
| By category | A 63, B 32, C 61, D 26 | A 70, B 31, C 52, D 38 |
| AI cost | US$8.15 | US$7.29 |
| Processing time | 35 min 56 s (AI run 1: 16.8 min, run 2: 18.2 min, grouping 51 s) | not recorded |
| Missing action | 0 | 0 |

## Fix confirmation
| Defect | Result |
|---|---|
| DEF-C19-1 hold reason exported | Confirmed: 10 Queries carry "Quoted evidence could not be located…"; 18 Queries are genuine (no hold) |
| DEF-C19-3 TBA grouped | Confirmed: one PH-TBA rule finding |
| DEF-C19-4 compound findings | No compound findings detected in issue text (heuristic check) |
| Timings recorded (DEF-C19-2) | Confirmed: 15 stages stored |

## Observations
- The Majors are consistent with check 19 (Reg 297 authorisation blank, Transperth endorsement contradiction, bus stop 28509, Appendix E empty, missing Appendix G, crane section N/A, TGS 05B beyond scope).
- **Processing time is the main issue:** 36 min for an 81-page TMP. The four passes run one after another, twice. With the queue (one check at a time) a second customer waits the full 36 min before their check starts.

## Recommendation
Run the four AI passes in parallel within each run (same requests, same cost). Expected ~6–7 min per run, ~13–15 min per check. Rate-limit retries (max_retries=6) are already in place. Needs a timing test on the next BC 016 run.

## Still needed
Tara's dispositions for precision (both runs).

# FB-01 — Reviewer feedback on SU025 Kanimbla Road check (Tara, WTGTM)

Received via Owner 2026-11-24. Partial: Q5 (errors / misses) deferred by Tara to "tomorrow".
Note: the SU025 report and annotated PDF were produced outside the repository; neither is held here.

| Q | Answer (verbatim summary) | AI-PM interpretation | Evidence class |
|---|---|---|---|
| 1 Review time | ~5 h, depends on complexity | Baseline for time-saving claim | Verified (customer statement) |
| 2 Volume | Produces 2 TMPs/week; does not review for others | ~8–9 TMPs/month ≈ 40–45 h/month | Verified (customer statement) |
| 3 Not caught | "No works on the road… no holes or trenching, workers on the verge, off the road; traffic counts not consistent during the day, peak 8am & 5pm, workers are finished" | **Ambiguous.** Reads as a rebuttal of F-001/F-002 (site context makes them inapplicable), not a list of catches → possible false-positive Criticals | Assumption — confirm |
| 4 Act on | All — "legal document", breach exposure | High trust placed on output → false Criticals are costly; reinforces reviewer gate (A-15) | Verified |
| 5 Errors / misses | Deferred | — | Awaiting input |
| 6 Returns | Client once; council 0–4 rounds; she does not count council rounds as rework | Rework is not a selling point; value = time to first-pass quality | Verified |

## Implications
- If F-001/F-002 were inapplicable, the engine raised Critical findings without site-context grounding → breach of §2 "no unsupported Critical". Action: Criticals that depend on works location (carriageway vs verge) or traffic-volume timing must cite the TMP text establishing the condition, else downgrade to Query.
- "Does not review for others": confirms R-20 — Tara is a self-reviewer; RTM status still unsighted.
- Market: ~2 TMPs/week per designer; 5 h/TMP.

## Addendum 2026-11-24 — further feedback
Tara: "the most important part is the risk analysis… sort out a tool for that… what risks are expected."
Response: pass E (risk assessment review) added to `llm_checks.py`, with draft expected-risk prompt list `compliance/risk_catalogue.yaml` (18 hazards, v0.1, unreviewed). Missing expected risks are reported as Query only, and only where the TMP states the triggering activity; inapplicable risks (her SU025 point) reported as Moderate.

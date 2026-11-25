# Handover — attg (TMP Check)

**Date:** 2026-11-25
**Goal:** Get TMP Check to G4/G5: a working portal plus a benchmarked engine, validated by Tara.

**Done**
- All branches merged into `main`, now the single authoritative record. Clashing IDs renumbered (DECISIONS: ID reconciliation).
- BENCH-06: untuned single run reached 86% of the reference (95/110) at US$2.62 (`docs/reviews/BENCH-06_SU026_base_engine.md`).
- Portal output fixes from the check 14/15 review (DEF-C14-1 to 6): highlighting, merging with unfound quotes → Query, rule actions, the category E line.
- Interrupted checks are marked failed when the portal starts. Processing time is recorded per check and per stage.
- Incident: the live TMP BC 016 was sent to the AI before G6 (R-29). A-41 is the Owner's one-off exception allowing a full AI check of BC 016.

**In progress**
- Owner re-running BC 016 with AI passes A–D ×2 on the PC portal (`python -m uvicorn src.portal.app:app --port 8000`).

**Stripe (A-46) — sandbox code built, not yet run live**
- Built: `src/portal/payments.py`, `/billing/checkout`, `/stripe/webhook`, tests `tests/portal/test_payments.py` (66 pass). Stripe MCP planner could not connect (proxy), so the SDK was used directly.
- To run against the sandbox: save the `sk_test_` key for api.stripe.com (secure form), set `STRIPE_SECRET_KEY` (sk_test_… ) and `STRIPE_WEBHOOK_SECRET` (from `stripe listen --forward-to localhost:8000/stripe/webhook`), buy with card 4242 4242 4242 4242.
- Open: refund → admin adjustment process; Stripe tax/invoice wording while GST not registered (A-04).

**Next 3 steps**
1. Owner: when BC 016 finishes, send the findings.json, report and annotated PDFs, then `Remove-Item Env:TMPCHECK_AI_PASSES`.
2. AI-PM: review the BC 016 outputs and timings; confirm DEF-C14 fixes; Owner re-runs check 14 (SU 025).
3. Owner/WTGTM: adjudicate the extra BENCH-06 findings (precision) and the TGS Note 2 dispute.

**Open questions**
- Portal prices: do A-31 to A-33 ($349 base) replace A-23 in `config/portal.yaml`?
- Pass E category before it is enabled.
- Tara's ruling on SU 025 F-001/F-002 (R-28).
- Portal guard that allows the AI only on historical or anonymised documents (proposed, not built).

**Previously:** 2026-11-24: portal + engine at 92% recall (BENCH-05); Tara test instructions drafted.

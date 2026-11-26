# Handover — attg (TMP Check)

**Date:** 2026-11-25
**Goal:** Get TMP Check to G4/G5: a working portal plus a benchmarked engine, validated by Tara.

**Done**
- Stripe sandbox built and verified on your PC (A-46). Managed Payments off (A-47). Refunds: the admin records the credit adjustment (A-48). Live payments on hold until G5.
- Check queue: one check at a time; uploads reserve credits.
- Speed: BC 016 now takes about 8 min (was 36 min) and US$6 (was US$8.15), using the cache warm-up and parallel passes.
- Consistency labels on findings. Check 15: 128 found in both runs, 51 in one run; all 12 Majors confirmed.
- [PR #1](https://github.com/abovethetableglobal-au/TMP-Proof-Reader/pull/1) open on branch `claude/determined-curie-a43sdd`; 74 tests pass. Claude is watching it.

**In progress**
- Email to Tara: `docs/comms/EMAIL_Tara_check15_BC016_DRAFT.md`. Attach the check 15 report (DRAFT 6) and the annotated TMP (DRAFT 5).

**Next 3 steps**
1. Review and merge PR #1.
2. Publish the Tally form, add its link to the email, and send it to Tara.
3. Re-run SU 025 on the new build; then rule on the BENCH-06 findings with WTGTM.

**Open questions**
- Stripe account legal entity and ABN.
- Insurance details for A-43.
- G2: WTGTM transfer and confidentiality confirmation.
- Before G6, the queue needs a proper job queue (currently in-process and SQLite).

**PC run notes:** run the portal from the inner folder on port 8001. Set `ANTHROPIC_API_KEY` (the `sk-ant-api03-` secret, not the `apikey_` ID), `TMPCHECK_AI_PASSES=A,B,C,D` and the Stripe `sk_test_` key.

**Previously:** 2026-11-25: Stripe Option A approved; BC 016 re-run in progress.

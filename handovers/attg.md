# Handover — attg (TMP Check)

**Date:** 2026-11-27
**Goal:** Get TMP Check to G4/G5: a working portal plus a benchmarked engine, validated by Tara.

**Done**
- PR #1 merged. Check 15 email and Tally form sent to Tara. Entity ATTG and ABN recorded (A-49); WTGTM confirmation and insurance on file (A-50).
- A-51: reviewer accreditation added to the portal. **My Account** stores level, certificate number and expiry. Reviewers without current accreditation can't decide findings or issue finals. The final report shows the accreditation. 79 tests pass (commit `6eea3c0`).
- Gate 3 becomes unconditional once Tara enters her details.
- Report downloads added: download buttons and a ZIP on the check page, and a Download button in My Checks.

**In progress**
- Waiting for Tara's check 15 (BC 016) feedback via Tally.

**Next 3 steps**
1. On your PC: `git pull`, then restart the portal on port 8001. The new fields are added automatically.
2. Tara opens My Account and enters her accreditation. Then tell Claude, so G3 can be marked accepted.
3. Re-run SU 025 on the new build, then rule on the BENCH-06 findings with WTGTM.

**Open questions**
- Should admins be blocked from issuing finals? At present only customer reviewers are blocked.
- Before G6, the queue needs a proper job queue (currently in-process and SQLite).

**PC run notes:** run the portal from the inner folder on port 8001. Set `ANTHROPIC_API_KEY` (the `sk-ant-api03-` secret), `TMPCHECK_AI_PASSES=A,B,C,D` and the Stripe `sk_test_` key.

**Previously:** 2026-11-25: Stripe sandbox verified; BC 016 sped up to about 8 min; PR #1 opened.

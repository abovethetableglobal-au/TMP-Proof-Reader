# Handover — attg (TMP Check)

**Date:** 2026-11-26
**Goal:** Go-to-market launch campaign (L9): draft and mock up everything now; publish only after G8.

**Done**
- Campaign plan: `docs/GTM_CAMPAIGN_PLAN.md` (D-25).
- Owner approved P-21 to P-24 (A-51 to A-54): tagline is now "Check • Cite • Confident"; numbers held until G5; $0 paid media until G8; a rule that downgrades one-run Majors to Query must be built and tested before the "every Major confirmed" claim is used. Check 15's 12 Majors were all found in both runs, but no rule guarantees it yet.
- Claims register: `docs/marketing/GTM-01_CLAIMS_REGISTER.md`. Copy pack: `docs/marketing/GTM-02_COPY_PACK.md` (§6 has the FB/IG posts with hooks and CTAs).
- Mock-ups (D-28) on a private canvas: https://claude.ai/artifact/Drdy696CM9kJaeiz6Ww4an (landing page, one-pager, LinkedIn post, email 1, three FB/IG feed posts, one story).

**In progress**
- All of the above: Ready for user review. Branch `claude/great-ride-f37rz2`, pushed. No PR yet.

**Next 3 steps**
1. Owner reviews the canvas and copy; list any changes.
2. Mock up LinkedIn posts 2–4 and emails 2–3, or build the anonymised demo report (GTM-03).
3. Build and test the one-run-Major → Query rule (A-54).

**Open questions**
- Tara technical review of the copy: on hold (Owner).
- Contact email and website for the placeholders.
- A-17 condition (Tara's accreditation details) is still open.

**PC run notes:** run the portal from the inner folder on port 8001. Set `ANTHROPIC_API_KEY` (the `sk-ant-api03-` secret), `TMPCHECK_AI_PASSES=A,B,C,D` and the Stripe `sk_test_` key.

**Previously:** 2026-11-25: G4/G5 portal and engine work; PR #1 merge approved, email to Tara sent.

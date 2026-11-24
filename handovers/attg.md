# Handover — attg (TMP Check)

**Date:** 2026-11-24
**Goal:** Get the TMP Check prototype to Gate 4/5: a working portal plus a benchmarked checking engine, validated by Tara.

**Done**
- Portal (local, Windows): dashboard, sign-in/roles/CSRF/audit (S2), upload → checks → draft → reviewer decisions → final. Decisions A-21–A-27.
- Engine: AI passes ×2 + grouping + rule checks → 92% recall on SU026, 1 FP, US$4.86/check (BENCH-05).
- Report PDF and annotated TMP built (D-11, D-12).
- Tara instructions drafted: `docs/outbound/TMP_Check_Reviewer_Test_Tara_v0.1.docx` (D-23).

**In progress**
- Owner reviewing check 8 outputs (Report PDF / Annotated TMP drafts).
- Branch `claude/gifted-gauss-ciwhyy` (not merged to main).

**Next 3 steps**
1. Owner: create Tara's account (`devseed … --role customer_reviewer`), send D-23, run timed screen-share review of check 8.
2. AI-PM: score Tara's decisions + time (TEST_REGISTER); tune grouping if > 45 min.
3. Owner: G4 sign-off; source ≥ 4 more WTGTM TMPs with reference reports for G5.

**Open questions**
- Owner feedback on report/annotation layout.
- Pending decisions: P-06 (AS 1742.3 licence), P-07 (credit gaps), P-08 (data residency), P-09 (pilot terms); A-17 conditions (Tara accreditation details + review pack) due 2026-11-27.

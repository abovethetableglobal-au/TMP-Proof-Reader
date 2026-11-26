# DELIVERABLES — Register (Master Prompt §19)

Repo: https://github.com/abovethetableglobal-au/TMP-Proof-Reader · Status labels per §11.2.

| ID | Name | Ver | Owner | Status | Approval | Location | Dependencies |
|---|---|---|---|---|---|---|---|
| D-00 | Master Prompt v1.4 (governing) | 1.4 | Owner | User accepted | Approved (A-12) | `MASTER_PROMPT_v1.4.md` | — |
| D-01 | Project handover brief | 1.0 | Owner | User accepted | Approved | `PROJECT_HANDOVER.md` | — |
| D-02 | Project records set (CLAUDE, BRIEF, PLAN, LOG, DECISIONS, RISKS, COMPLIANCE_REGISTER, AI_RESOURCES, TEST_REGISTER, COMMERCIAL_MODEL, HANDOVER, DELIVERABLES) | 0.2 | AI-PM | User accepted | Approved (A-13) | repo root | — |
| D-03 | WTGTM evidence request | 0.2 | AI-PM | User accepted | Approved (A-14) | `docs/WTGTM_EVIDENCE_REQUEST.md` | — |
| D-04 | Test methodology | 0.1 | AI-PM | User accepted | Approved (A-13) | `docs/TEST_METHODOLOGY.md` | P-03 |
| D-05 | Prototype architecture | 0.1 | AI-PM | User accepted | Approved (A-13) | `docs/ARCHITECTURE.md` | P-04 |
| D-06 | Compliance rule schema | 0.1 | AI-PM | Production complete | Not approved | `compliance/rules/_schema.yaml` | — |
| D-07 | TPR-01 three-perspective review (simulated) | 1.0 | AI-PM | User accepted | Approved (A-13) | `docs/reviews/TPR-01_project_strategy.md` | — |
| D-08 | IR-01 independent review brief | 1.0 | AI-PM | Awaiting approval | Pending (Owner transfer) | `docs/handovers/IR-01_independent_strategy_review.md` | — |
| D-09 | WA compliance rule library (initial) | 0.1 | AI-PM + Tara | User accepted (conditional, A-17) | Not approved | `compliance/rules/` | Tara review; P-06 |
| D-10 | Prototype pipeline | 0.1 | AI-PM | In progress (template-diff, deterministic checks v0.2, LLM passes A–D coded & wiring-tested; awaiting API key) | Not approved | `src/tmpcheck/` | API key; WTGTM evidence |
| D-11 | Report PDF (Output 1) | 0.1 | AI-PM | Quality checked (synthetic sample; 36 tests) | Not approved | `src/tmpcheck/outputs.py`; example `test-library/samples/outputs/` | D-10 |
| D-12 | Annotated PDF (Output 2) | 0.1 | AI-PM | Quality checked (synthetic sample) | Not approved | `src/tmpcheck/outputs.py`; example `test-library/samples/outputs/` | D-10 |
| D-14 | Spike S-01 (extraction, completeness, annotation) | 0.1 | AI-PM | Quality checked | n/a (internal) | `src/spike/`, `docs/reviews/SPIKE-S01_results.md` | — |
| D-15 | Rule review pack for Tara | 0.1 | AI-PM | User accepted | Completed by reviewer | `docs/outbound/TMP_Check_Rule_Review_Tara_v0.1.docx` | D-09 |
| D-16 | G2 evidence analysis 01 (REF-01) | 0.1 | AI-PM | Ready for user review | Pending | `docs/requirements/G2_EVIDENCE_ANALYSIS_01.md` | WTGTM evidence |
| D-17 | Customer portal dashboard implementation plan | 0.1 | AI-PM | Awaiting approval | Pending (P-12–P-16) | `docs/DASHBOARD_IMPLEMENTATION_PLAN.md` | Owner brief + mock-up 2026-11-20 |
| D-18 | Customer portal — S1 shell + S4 upload/check + reviewer workflow | 0.2 | AI-PM | Ready for user review | Pending | `src/portal/`, `config/portal.yaml`, `tests/portal/` | A-21, A-22 |
| D-19 | BENCH-02 engine benchmark (SU026) | 0.1 | AI-PM | Under review | Pending (Tara confirmation) | `docs/reviews/BENCH-02_SU026_AI_passes.md` | OWNER-FT-02 |
| D-20 | BENCH-03 tuned engine benchmark (SU026) | 0.1 | AI-PM | Under review | Pending (Tara confirmation) | `docs/reviews/BENCH-03_SU026_tuned.md` | D-19 |
| D-21 | BENCH-04 repeat-run variance (SU026) | 0.1 | AI-PM | Under review | Pending | `docs/reviews/BENCH-04_SU026_repeat_run.md` | D-20 |
| D-22 | BENCH-05 two-run benchmark (SU026) | 0.1 | AI-PM | Under review | Pending (Tara confirmation) | `docs/reviews/BENCH-05_SU026_two_run.md` | A-27 |
| D-23 | Reviewer test instructions for Tara (timed review of check 8) | 0.1 | AI-PM | Awaiting approval | Owner to approve and send (CLAUDE.md §1) | `docs/outbound/TMP_Check_Reviewer_Test_Tara_v0.1.docx` | S2, check 8 |
| D-13 | Data-handling statement | — | AI-PM | Not started | — | TBC | P-04, P-08 |
| D-24 | BENCH-06 LLM benchmark vs REF-01 | 0.1 | AI-PM | Quality checked | Pending | `docs/reviews/BENCH-06_SU026_base_engine.md` | REF-01, API key |
| D-25 | Go-to-market launch campaign plan | 0.1 | AI-PM | Ready for user review | Pending (P-21–P-24) | `docs/GTM_CAMPAIGN_PLAN.md` | L9, G5–G8 |
| D-26 | GTM-01 Claims and substantiation register | 0.1 | AI-PM | Ready for user review | Pending | `docs/marketing/GTM-01_CLAIMS_REGISTER.md` | D-25 |
| D-27 | GTM-02 Copy pack (landing, one-pager, emails, LinkedIn) | 0.1 | AI-PM | Ready for user review | Pending (P-21, G5) | `docs/marketing/GTM-02_COPY_PACK.md` | D-26 |
| D-28 | GTM mock-ups (landing page, A4 one-pager, LinkedIn launch post, email 1) | 0.1 | AI-PM | Ready for user review | Pending | Design canvas https://claude.ai/artifact/Drdy696CM9kJaeiz6Ww4an (private) | D-27 |

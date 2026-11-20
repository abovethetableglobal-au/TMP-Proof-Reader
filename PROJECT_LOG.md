# PROJECT_LOG — TMP Check

## 2026-11-20 — Project initiation (AI-PM)
**Completed**
- Workspace `TMP-Check/` created; local git repo initialised; `customer-docs/` git-ignored.
- Handover saved as `PROJECT_HANDOVER.md`; all §15 project files created.
- Approved commercial/product decisions recorded (DECISIONS A-01–A-10); 9 pending Owner decisions raised.
- Risk register: 15 risks; top 3 = R-02 mis-citation, R-03 review cost vs $149 credit, R-01 missed safety issue.
- WA regulatory research (WS3): WA Code March 2026 located on mainroads.wa.gov.au; adopted editions identified (AGTTM Ed 1.1 Pts 1–7,9,10; Ed 2.0 Pt 8; AS 1742.3–2019). Version-control finding VC-01: WA has not adopted AGTTM Ed 1.2.
- Compliance rule schema v0.1; source register with 11 sources.
- WTGTM evidence request drafted (`docs/WTGTM_EVIDENCE_REQUEST.md`).
- Test methodology v0.1; lowest-cost architecture v0.1.

**Issues**
- Master Prompt v1.4 not supplied (P-01).
- No remote repository — records at risk when container is reclaimed (P-02 / R-13).
- WA Code section content was AI-extracted; manual clause verification still required.

**Next actions**
1. Owner: P-02 repo, approve/send evidence request, decide P-01, P-03, P-04.
2. AI-PM: manually verify Code §4.2 clauses; draft first rules (status draft-unverified).
3. AI-PM: extraction/annotation spike on public MRWA TMP template.

## 2026-11-20 — Repository established (AI-PM)
- Private repo `abovethetableglobal-au/TMP-Proof-Reader` created by Owner and connected; initial commit pushed. P-02 resolved (A-11); R-13 closed.
- Open: P-01 Master Prompt v1.4; P-03 reviewer; P-04 AI provider; WTGTM evidence request awaiting Owner approval.

## 2026-11-20 — Master Prompt v1.4 adopted (AI-PM)
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Save Master Prompt v1.4; import into CLAUDE.md; fix hierarchy to §6.1 | AI-PM | Production complete | — | — |
| Three-perspective review TPR-01 (simulated) | AI-PM | Ready for user review | — | Owner approves baseline (P-10) |
| Independent review brief IR-01 | AI-PM | Awaiting approval | Owner transfer | Owner pastes to ChatGPT/Gemini |
| Deliverable register; capability register; budget table; §11.2 status labels | AI-PM | Production complete | — | — |
| Project baseline | Owner | Awaiting approval | — | P-10 |

**Issues:** none new. **Approvals pending:** P-03–P-10.

## 2026-11-20 — Gate 1 passed
- Owner approved baseline Option A (A-13). G1 = User accepted.
- Next: WS3 core rule drafting; WS6 technical spike on public MRWA TMP template.

## 2026-11-20 — WS6 Spike S-01
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Spike S-01 on public MRWA TMP template | AI-PM | Quality checked | — | Template-diff design once WTGTM templates (A5) arrive |
| Core rule drafting (Code §3.5, §4.2, §8) | AI-PM | Not started | Manual Code verification | Next work item |

Result: 32 evidence-bound findings, original unchanged, 3 defects found and fixed, 3 gaps logged. Key learning: completeness should be a template-diff against WTGTM templates — raises priority of evidence item A5.

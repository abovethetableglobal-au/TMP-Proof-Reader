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

## 2026-11-20 — Evidence request approved
- A-14: request v0.2 approved; blank templates now item A4 (Essential). Owner to send. G2 clock starts on send.

## 2026-11-20 — Change: self-approve operating model (Master Prompt §20.1)
| Item | Assessment |
|---|---|
| Change | Customer's accredited person (Tara, WTGTM) reviews and approves each report; TMP Check issues draft → final after review |
| Reason | Owner direction; matches WTGTM retaining professional responsibility |
| Scope | No change to product scope; review workflow moves into customer portal |
| Budget | Removes reviewer cost from TMP Check; contribution ≈ $128–143/credit (estimate) |
| Timeline | Removes reviewer-appointment blocker on G3/G5 |
| Quality | New risks R-16 (automation bias), R-17 (independence), R-18 (single reviewer), R-19 (blind ground truth) |
| Affected | CLAUDE.md §2, ARCHITECTURE, TEST_METHODOLOGY, COMMERCIAL_MODEL, RISKS, PLAN, AI_RESOURCES |

## 2026-11-20 — WS3 core rules + reviewer accreditation
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Record Tara's accreditation as unverified assumption (S-07, R-20) | AI-PM | Production complete | — | Sight records before G3 |
| Draft rules from WA Code §3.5, §4.2.1–4.2.3 (primary text, local PDF extraction, no Firecrawl spend) | AI-PM | Production complete (17 rules) | — | §8 accreditation rules |
| Tara review of rule set | Tara | Not started | Rule set complete | G3 |

Finding: Code §4.2.1 mandates use of a Main Roads TMP template with headings retained (VC-04) — confirms template-diff approach.

## 2026-11-20 — Claude API approved (A-16); environment set up
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Personal cloud environment `TMP-Proof-Reader` created; session moved onto it | AI-PM (Owner approved) | Production complete | — | Setup script proven on next fresh session |
| Claude API key | Owner | Awaiting input | — | Add env var `ANTHROPIC_API_KEY` in environment settings; start a new session |
| §8 accreditation rules | AI-PM | Not started | — | Next |

## 2026-11-20 — Security incident + §8 rules
- **Incident:** Owner pasted an Anthropic token into chat. Not used or stored by AI-PM; Owner revoked it (R-21, closed). Key to be supplied via `ANTHROPIC_API_KEY` env var in TMP-Proof-Reader environment.
- **WS3:** 5 rules added from Code §4.2.3 and §8 → 22 rules, core set ready for Tara review (G3).

## 2026-11-20 — Rule review complete
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Tara review of 22 core rules | Tara (via Owner) | User accepted — all accepted as written | — | — |
| Reviewer accreditation details (S-07) | Owner / Tara | Awaiting input | — | Provide level, number, expiry |
| Gate 3 sign-off | Owner | Awaiting approval | S-07 | Owner decision |
Note: review outcome relayed verbally by Owner; completed review pack not yet on file.

## 2026-11-20 — Gate 3 passed (conditional)
- A-17. Conditions due 2026-11-27: Tara accreditation details + completed review pack.
- Next: G4 prototype — rule engine + template-diff completeness on public template (no API key needed); LLM checks once key is configured.

## 2026-11-20 — G4: template-diff completeness module
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| `src/tmpcheck/template_diff.py` (rule WA-COP-4.2.1-001) | AI-PM | Quality checked | — | Integrate into pipeline |
| Seeded test T-SEED-01 | AI-PM | Production complete | — | Add seeds for other rules |
Result TD-01: 3/3 missing headings found, 0 false positives (109-heading control), stale TOC ignored.
Known limitations: very short headings (e.g. 'Roles', 'Public') could match unrelated body lines → possible missed finding; heading present but section body empty is not yet checked.
Observation: the MRWA template itself contains a typo in a heading ('Existing Traffic and Adverting Signs'). Proofreading must not penalise text the Code requires users to retain; flag as Minor 'template-originated' at most.

## 2026-11-20 — WTGTM evidence returned
- Owner reports WTGTM returned the evidence pack today. Not yet transferred to AI-PM.
- Before handling: confirm anonymised, or WTGTM written permission (Handover §13 Phase 1; CLAUDE.md §3). Store only in git-ignored `customer-docs/`.
- Owner reports WTGTM gave **verbal** permission to use original (non-anonymised) documents. Conflicts with request v0.2 wording (written permission) and A-16 (anonymised docs only before G6) — raised to Owner as P-11.
- A-18: Owner chose Option C — proceed on verbal permission (R-22). Awaiting upload.

## 2026-11-20 — First evidence item analysed (REF-01)
- Received 1 file: a 4-page proofread report (~105 findings) on a 61-page TMP. The TMP itself was not supplied.
- 16 new engine requirements (RQ-01–RQ-16) derived; report layout recommended as base for Output 1.
- Provenance flag: metadata shows Owner's business as author, code-generated PDF; must confirm who produced it before using it as ground truth.
- Customer name discrepancy flagged: 'Way to Go' (report) vs 'Way Too Go' (brief).
- A-19: REF-01 confirmed correct → usable as reference findings. A-20: customer name corrected to 'Way to Go Traffic Management' across records; rule review pack and evidence request source files updated (copies already sent keep the old spelling).

## 2026-11-20 — BENCH-01: first benchmark on a real TMP
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Deterministic checks v0.2 on REF-01 source TMP | AI-PM | Quality checked | — | — |
| Adjudicate 3 repeated-sentence findings | Owner | User accepted — ignore (excluded from scoring) | — | — |
| LLM pass (categories A, B, D) | AI-PM | Blocked | ANTHROPIC_API_KEY env var + new session | Owner adds key |
Result: 9/26 template leftovers found, 0 false positives, 1 extra valid issue. ~95 of ~105 reference items need the LLM pass.

## 2026-11-20 — LLM checking passes coded (G4)
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| `src/tmpcheck/llm_checks.py` — passes A (proofreading), B (consistency), C (semantic leftovers), D (TGS drawings, vision) | AI-PM | Production complete — request accepted by SDK and API (401 with dummy key) | API key | Run on REF-01-SRC and score vs ~105 reference findings |
Design: claude-opus-5-5, effort high, PDF document block cached across passes, Pydantic structured output, evidence validation (unverifiable quotes downgraded to Query), server-side refusal fallback, per-pass cost logging.
Estimated cost per 61-page TMP (estimate, to be measured): ~US$2–4 for 4 passes.

## 2026-11-24 — FB-01 reviewer feedback (SU025) + external research received
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Record Tara feedback (`docs/reviews/FB-01_Tara_SU025.md`) | AI-PM | Production complete | — | — |
| Confirm whether Q3 answer means F-001/F-002 are wrong | Owner → Tara | Awaiting input | Tara Q5 reply | Owner asks Tara |
| Ground site-dependent Criticals in TMP text (else Query) | AI-PM | Not started | Confirmation above | Change C-pass prompt + evidence validator |
| Copilot market research (TMP volumes, RTM count) | Copilot (via Owner) | Under review | — | Verify RTM count against MRWA register |
| BENCH-02 | AI-PM | Blocked | API key env var; re-upload SU026 files | — |
Copilot research classification: TMP annual volume — no source (Copilot's own "20,000+" is an unverified estimate); RTM ~40–50 — source-supported, unverified by AI-PM; City of Perth ~300 permits/month — unverified. Copilot's "pivot to RTM reviewers / AI-generated TMPs" is a scope change → P-12.

## 2026-11-24 — Pass E: risk assessment review
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Pass E in `llm_checks.py` (missing / inapplicable risks, controls not carried through, rating checks) | AI-PM | Production complete — not run | API key | Run in BENCH-02 |
| `compliance/risk_catalogue.yaml` v0.1 (18 expected hazards) | AI-PM | Ready for user review | — | Tara review: add/remove/reword hazards and triggers |
Trigger: Tara feedback — risk analysis is the most important part. In scope (document QA of an existing section); no design or site assumptions.
| Realign risk catalogue to AGTTM Part 2 (AGTTM02-26 Ed 1.2) Appendix B "TMP Risk Considerations Checklist" | AI-PM | Awaiting input | Owner downloads free PDF (site blocks automated download) | Map items, cite source/edition/appendix |
| Risk catalogue v0.2: 34 items from AGTTM02-26 Table B.1 + 8 supplementary worker-safety items | AI-PM | Ready for user review | Tara review; Ed 1.1 comparison | Owner supplies AGTTM02-21 (Ed 1.1) |
| Ed 1.1 vs Ed 1.2 Table B1 comparison | AI-PM | Quality checked — word-for-word identical (765/765 words; layout only) | — | Catalogue v0.3 cites WA-adopted Ed 1.1 |

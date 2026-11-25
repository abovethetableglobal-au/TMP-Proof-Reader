# PROJECT_LOG — TMP Check

## 2026-11-25 — Portal output fixes from the check 14/15 review (AI-PM)
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Merge `g4-postprocess-fixes` (D1–D5) into the portal line | AI-PM | Production complete | — | Owner functional test on PC |
| Fix DEF-C14-1 to DEF-C14-6 (TEST_REGISTER) | AI-PM | Quality checked — 53/53 tests pass; check 14 data: 147/149 text findings highlighted (was 118) | — | Re-run check 14 on Owner's PC |
| Reconcile divergent records across branches | Owner | Awaiting approval | — | See Issues |
Branch `claude/portal-postprocess-fixes` = `claude/fervent-hopper-q3h87z` + `g4-postprocess-fixes` + these fixes.
**Issues:** project records have diverged across branches. DECISIONS IDs A-21 and A-22 mean different things on the portal line and the g4 line (kept here as "A-21 (g4 line)" and "A-22 (g4 line)"), and `claude/blissful-davinci-884my9` uses A-21 to A-31 again. BENCH-02 to 05 exist on the portal line; BENCH-06 (an untuned engine re-run, 86% recall, US$2.62) is on `claude/llm-pass-ref-01-src-jys8ll`. One authoritative line (main) is needed (Master Prompt §11.4).
Check 15 was run on a TMP Check report, not a TMP. Its findings 256/257 (a "FINAL" banner and mismatched margin severities) do not reproduce on check 14.

## 2026-11-25 — G4 pipeline defect fixes (AI-PM)
**Completed**
- Key check (HANDOVER step 1): `ANTHROPIC_API_KEY` **not set** in session (`False`). Network secrets cannot be used for api.anthropic.com; Owner to enter the value as an environment variable. LLM passes A–D **Blocked**.
- Owner confirmed SU_025 Kanimbla Road is historical (DECISIONS A-21).
- New `src/tmpcheck/postprocess.py`, wired into `llm_checks.py` and `det_checks.py`. Fixes from the prior draft-report review:
  - D1 validator now uses the same word-level locator as annotation; unlocatable quotes → Query / Unable to verify (bbox stored when found).
  - D2 VISUAL-only Critical findings held as Query (`original_severity`, `hold_reason` kept for reviewer).
  - D3 outcome derived from severity: Query → "Unable to verify", else "Potential issue".
  - D4 duplicate findings merged across passes/pages (`merged_from`); rule findings merge only on same rule + evidence + page.
  - D5 DUP-SENT: TGS sheets detected by title block (not only landscape) and excluded; category changed A Proofreading → C Completeness (RQ-06).
- Tests: `tests/test_postprocess.py` (synthetic PDF), 6/6 pass.
- SU_025 received (git-ignored). D5 refined: SU_025 TGS sheets are portrait Letter pages without 'TGS' text; detection now uses title-block fields. Deterministic run: DUP-SENT 9→3, PG-HEADER 3→1.
- Owner approved ≤US$5 API spend (A-22). Key added by Owner but not visible in this session (env vars load at session start) — run deferred to next session.
**Not done**
- D6 (PDF report rendering: ghost table shading/borders, orphaned headers): no report renderer in the repository — Awaiting input (source of the reviewed draft report).
- G4 passes A–D on SU_025 and cost per pass: Blocked (API key; PDF not yet uploaded).

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

## 2026-11-20 — Dashboard UI brief received
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Repository review + dashboard implementation plan (D-17) | AI-PM | Awaiting approval | P-12–P-16 | Owner decides P-12 |
| Portal stages S1–S7 | AI-PM | Not started | P-12, P-13 | — |
Ten conflicts identified (plan §2): portal timing vs S-03, "Compliant" wording vs CLAUDE.md §2, purchase UI vs A-09, 5-pack vs P-05, "Completed" status vs reviewer gate (A-15), credit consumption point, savings baseline. C-6, C-7, C-10 applied as safety/record corrections; remainder raised as P-12–P-16. Risks R-23, R-24 added.
- A-21: Owner approved local portal build S1–S4 in parallel (P-12 resolved).
- A-22: Owner approved headline "Fast. Thorough. Evidence-based." (P-13 resolved). Starting S1.

## 2026-11-20 — Portal stage S1 (shell) built
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| S1 shell: FastAPI + Jinja, 6 pages, live-data dashboard with empty states, responsive (1536/1024/390 px, no horizontal overflow), Compliance Library from 22 approved rules | AI-PM | Quality checked (15/15 tests) | — | Owner review of screenshots |
| S2 accounts (login, roles, tenant tests, audit log) | AI-PM | Not started | — | Next build stage |
| S3 ledger + purchase flow | AI-PM | Awaiting approval | P-14, P-15 | — |
Applied: A-22 headline; statuses per plan C-6/C-7; 5-pack hidden (`offered: false`) pending P-14; purchase buttons = manual credit request (A-09); savings card empty until baseline (P-16 default). Banner is an SVG illustration — no licensed photo used (no spend). Upload validates type/size/signature client-side only; server upload is S4.
Limitations: no authentication (app refuses to start unless TMPCHECK_ENV=local); "Contact us" details not yet set.
- A-23: manual-invoice credit requests; 5-pack $745 offered (P-14, P-05 resolved). `CR-5 offered: true`.
- A-24: credit consumed on draft delivery to reviewer (P-15 resolved). S3 unblocked; P-16 (savings baseline) remains, card defaults to empty state.
- A-25: Potential Savings card removed; replaced by "Awaiting Review" card (P-16 resolved). All dashboard decisions closed; S2 next.
- Owner instruction: subscription price removed from dashboard Subscription tile (status only). Price still shown on Credits & Billing.
- Owner instruction: Subscription tile shows status as the headline value (Active in green; Not active/Lapsed/Cancelled in grey).
- Added `src/portal/devtools.py` so the Owner can switch the local test account between states (subscription, credits, checks). Local DB only.

## 2026-11-20 — Portal functional slice (S4 + S5-lite)
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Upload → server validation → stored original (git-ignored) → deterministic checks (+ AI passes if `TMPCHECK_AI_PASSES` and API key set) → draft → credit consumed (A-24) | AI-PM | Quality checked | — | Owner functional test |
| Reviewer workflow: accept / edit (note required) / reject per finding; final blocked until all decided (A-15) | AI-PM | Quality checked | — | Reviewer role enforcement in S2 |
| Credit history from ledger on Credits & Billing | AI-PM | Quality checked | — | — |
| Synthetic sample `test-library/samples/SAMPLE-TMP-01.pdf` (7 seeded issues, no customer data) | AI-PM | Quality checked | — | — |
Not yet: report PDF (D-11), annotated PDF (D-12), sign-in/roles (S2), CSRF protection (S2). Fixed Windows crash: `%-d` date format replaced with portable filter.
- A-26: SU026 (61 pp: 50 + 11 drawings) rejected under A-10 on Owner test. Owner approved single 100-page limit incl. drawings.
- OWNER-FT-01: Owner ran SU026 end to end in local portal (rule-based only, 21 findings, final issued). AI passes not active in that run.
- Owner second SU026 run again had no AI passes (silent skip). Portal now prints AI status at startup and records why passes were skipped on the check page.
- OWNER-FT-02: AI passes ran on SU026 (293 raw findings, US$3.33). Added duplicate merging across checks, AI fix/category mapping, findings JSON export for benchmarking.
- Dedupe on SU026 check 5: 293 → 211 findings (82 duplicates merged, 28%). Still ~2× REF-01 (~105); BENCH-02 scoring needed to separate genuine extras from noise.

## 2026-11-20 — BENCH-02 scored
- Recall 88% (97/110) vs REF-01, 3 likely false positives, US$3.33. Main gap is noise: 211 findings → est. 70–105 min review vs 45 min target (R-03). Actions: cross-page grouping, style roll-up, pass A punctuation, pass D placement → Query. Scoring is simulated; Tara to confirm extras.

## 2026-11-20 — BENCH-02 actions 1–3 implemented
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Cross-page/cross-pass issue grouping (one text-only Claude call; returns id groups only, never edits findings) + style roll-up into one finding | AI-PM | Quality checked (unit tests, fake API client) | Live API | Owner: `devtools consolidate 5` (~US$0.15), then BENCH-03 re-run |
| Pass A punctuation checklist; style variants one-per-term; pass B one report per conflict; pass D placement → Query, body figures added | AI-PM | Production complete | Live API | BENCH-03 |
| DUP-SENT rule → Query / Unable to verify (Owner excluded type in BENCH-01) | AI-PM | Quality checked | — | — |
| `pages` field (all pages an issue affects); SQLite auto-adds new columns to existing local DBs | AI-PM | Quality checked | — | — |
Not live-tested: no API key in the AI-PM environment. Consolidation failure falls back to ungrouped findings.
- Owner ran `devtools consolidate 5`: 211 → 138 findings (6 Major, 30 Moderate, 95 Minor, 7 Query) for US$0.18 (total US$3.51). Observed possible over-merge: p25 consultation placeholders grouped with p57 empty Appendix E (REF-01 lists them separately). Scoring pending JSON export.
- BENCH-02b: grouping cut check 5 to 138 findings with no loss of reference items (89% recall); 3 over-merges → grouping prompt tightened. Next: BENCH-03 full re-run with new prompts.

## 2026-11-20 — BENCH-03 scored
- Tuned engine on SU026: 124 findings, 88% recall, ~0 false positives, est. 41–62 min review, US$2.75. Run-to-run variance ±7 items noted (supports human review gate). Next: D-11 report PDF, D-12 annotated PDF to complete G4 criteria.
- BENCH-04: Owner re-ran SU026 (check 7): 84% alone; union with check 6 = 91%; with check 5 = 96%. Supports "2 runs + grouping" (option A). Awaiting Owner go-ahead.

## 2026-11-20 — Two-run default (BENCH-04 option A, Owner approved)
- AI passes now run twice per check (`config/portal.yaml` ai.runs: 2; env TMPCHECK_AI_RUNS overrides, max 3); findings combined, merged and grouped; cost summed.
- New rule checks: run-together words ("upto"), split words ("week s"), missing space after "No." — items missed by every AI run.
- 35/35 portal tests pass. Next: Owner runs SU026 (≈US$5.40) → BENCH-05.
- BENCH-05: two-run default on SU026 = 92% recall, 152 findings, 1 FP, US$4.86. Recall target met; review time (51–76 min) is now the constraint. Next: D-11/D-12, then Tara times a real review.

## 2026-11-20 — Outputs 1 and 2 built (D-11, D-12)
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Report PDF: project/document details, scope A–E, compliance sources and editions, severity summary, numbered findings with evidence and suggested action, reviewer edits, matters for human review, limitations | AI-PM | Quality checked (sample) | — | Owner reviews on SU026 check 8 |
| Annotated TMP: copy of original, highlights + F-number labels at quoted text, margin notes for VISUAL/unlocated and related pages; no pages added; original text unchanged | AI-PM | Quality checked (sample) | — | Owner reviews on SU026 |
| Draft outputs watermarked DRAFT, generated on demand; finals generated and stored at issue (fixed record), rejected findings excluded, reviewer named | AI-PM | Quality checked | — | — |
PyMuPDF only (no new dependency; WeasyPrint not needed — avoids GTK install on Windows). G4 criteria now met in prototype form, subject to Owner review of the SU026 outputs.

## 2026-11-21 — Portal stage S2: sign-in, roles, CSRF, audit log
| Task | Owner / AI | Status | Dependencies | Next step |
|---|---|---|---|---|
| Sign-in with email + password (scrypt hashes, 10+ chars, 5-failure lockout), server-side sessions (12 h, HttpOnly, SameSite=Lax, only token hash stored), sign-out | AI-PM | Quality checked | — | Owner sets password via devseed |
| Roles: customer_user (upload/view) vs customer_reviewer/admin (decide findings, issue final) — enforces A-15 in the portal | AI-PM | Quality checked | — | — |
| CSRF token on every POST (form field or header) | AI-PM | Quality checked | — | — |
| Audit log (append-only): login, failed login, upload, view, downloads, exports, decisions, final issue, cross-organisation access attempts | AI-PM | Quality checked | — | Admin view later |
39/39 portal tests (incl. signed-out redirect, wrong password, missing CSRF → 403, user role → 403, other organisation → 404 + audit). Standard library only (no new dependency). Still local-only; hosting needs G6 security review (penetration test, HTTPS, data-handling approval).
- Fix: upgrading a pre-S2 local database added the new `active` column as empty, which would have blocked sign-in. New columns now get their default; empty treated as active. Tested on a simulated old database.
- Owner signed in to the S2 portal on Windows after upgrade (existing data intact: 5 SU026 drafts, 93 test credits). S2 user-accepted for local use pending Owner confirmation.
- D-23 drafted: one-page reviewer test instructions for Tara (screen-share method, no data leaves Owner PC). Awaiting Owner approval to send.

## 2026-11-24 — attg resumed; AI-PM review of check 8 drafts
- Branch `claude/gifted-gauss-ciwhyy` fast-forwarded into `claude/fervent-hopper-q3h87z`.
- Owner re-uploaded check 8 Report PDF + Annotated TMP drafts (stored in git-ignored `customer-docs/wtgtm-2026-11-24/`).
- AI-PM review (simulated, single model): 10 defects raised (rule-tag misattribution after grouping, non-standalone finding text, Query/Potential-issue label mismatch, excluded repeated-sentence findings reappearing, truncated quotes, ghost table rows, related-note stacks obscuring TMP/TGS content). Status: Revision required. Awaiting Owner layout feedback before fixing.

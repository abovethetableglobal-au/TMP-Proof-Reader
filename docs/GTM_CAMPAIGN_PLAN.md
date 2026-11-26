# Go-to-Market Launch Campaign — TMP Check · v0.1 (2026-11-26)

**Status:** Ready for user review. Not approved.
**Tier:** Significant (§2A): external-facing, makes safety and performance claims, involves spend.
**Parent:** `docs/LAUNCH_PLAN.md` workstream L9 (A-34).
**Review method:** simulated three-perspective review (§5.3). No independent platform or person was used.

## 1. Project understanding
The campaign takes TMP Check from a single pilot customer (WTGTM) to paying WA traffic management companies. It must sell a document-QA service without claiming approval, compliance or safety. Public launch can only follow G8 (provisional date 2027-05-17). Everything before G8 is preparation, plus a soft launch to WTGTM from G7.

## 2. Objectives
| # | Objective | Measure |
|---|---|---|
| O1 | Convert WTGTM from pilot to a paying customer | Subscription and first pack bought within 30 days of G8 |
| O2 | Sign further WA TM companies | 3 paying customers by G8 + 90 days (assumption; set with Owner) |
| O3 | Win reviewer trust | ≥ 5 accredited reviewers trial a demo report |
| O4 | Zero claims breaches | 0 published items using banned wording or unsupported proof points |

## 3. Key considerations
**Verified facts from the repository (§18.2):**

| Claim in brief | What the record shows | Consequence |
|---|---|---|
| "About 8 min per 81-page TMP" | Checks 14 and 15 on BC 016 (81 pp) took 7 min 40 s and 7 min 51 s (PROJECT_LOG 2026-11-25). Engine time only. | Usable as "about 8 minutes processing for an 81-page TMP in testing". The reviewer's time must be stated separately: 51–76 min measured (BENCH-05). |
| "92% recall on benchmark (BENCH-05)" | One TMP (SU026, 61 pp), compared against one reference set (REF-01). Untuned single run: 86% (BENCH-06). | Too small a sample to publish before G5. Hold until the G5 multi-document benchmark. |
| "Every Major confirmed by two AI runs or a rule check" | **Not supported.** Check 15: 51 of 192 findings came from one run only, and there is no rule restricting Majors to two-run or rule-check findings. | Remove the claim, or build the rule and test it first (see P-24). |
| "22 WA Code of Practice rules signed off by an accredited reviewer" | A-17: Gate 3 signed off **conditionally**, for prototype use on test documents. Tara's accreditation details are due 2026-11-27 and still open (log 2026-11-26). | Do not publish until the A-17 condition is closed and the 22 rules are approved for live use (G6). |
| Tagline "Check • Comply • Confident" | Retained by Owner decision A-22. R-24 flags "Compliant" wording as High impact. | Conflicts with CLAUDE.md §2 (priority 1–2 over A-22). Decision needed: P-21. |

**Constraints:** no payments before G5 (CLAUDE.md §5); no external sending without the Owner; prices come from config; AS 1742.3 is deferred to G8 (R-26), so the copy must not imply full standards coverage.

**Opportunities:** reviewer time is the buyer's pain (Tara estimates 5+ h per TMP manually), so lead with "hours of desk-check reduced to a reviewer's disposition". A WTGTM case study and a referral from Tara are the strongest proof in a small, relationship-driven market.

## 4. Required expertise
| Perspective | Role in this campaign |
|---|---|
| B2B marketing strategist | Positioning, segmentation, channels and funnel |
| Content and creative director | Message hierarchy, copy, demo assets |
| Regulatory and claims-risk specialist (WA TM / ACL) | Substantiation of every claim, misleading-conduct risk, safety wording |

## 5. AI organisation and resources (verified availability)
| Resource | Use | Status |
|---|---|---|
| Claude Code (this session) | Strategy, copy, landing-page build, registers | Available |
| Canva MCP | Social creatives, one-pager layout | Tools listed; not yet tested in this project |
| HubSpot MCP | Contact list and email staging (send by Owner only) | Tools listed; account not verified |
| Tally MCP | Demo-request / lead form | In use (A-50 log) |
| WordPress.com MCP | Possible landing-page host | Listed; hosting decision pending (P-20) |
| Copilot (via Owner) | Market sizing (RTM count) | Under review, not verified |
| Tara (accredited reviewer) | Claims technical check, testimonial | Human; Owner sends requests |

## 6. Three-perspective review (simulated)
| Perspective | Finding |
|---|---|
| Strategist | The market is small: dozens of WA TM firms, roughly 2 TMPs/week per designer (FB-01). Direct outreach plus referrals beats paid ads. The 12-month credit expiry and 10-pack suit firms with steady volume. |
| Creative | The headline is strong. "Comply" in the tagline contradicts the "evidence-based" positioning. A real annotated sample page shows the product better than any statistic. |
| Claims-risk | Under the ACL (s18, s29), a percentage or a "signed off" claim needs substantiation at the time it is published. Single-document statistics and a conditional sign-off do not meet that test. One false claim ("every Major confirmed…") is already in the brief. |

**Consolidated recommendation:** run a proof-led, relationship-first campaign. Hold every quantitative claim until G5 evidence exists. Replace "Comply". Remove the two-run claim unless it is built and tested. No paid media at launch.

## 7. Recommended strategy
| Phase | Window | Activities | Gate dependency |
|---|---|---|---|
| 0 Prepare | Now – G5 | Claims register; copy pack v0.1; anonymised demo report; landing-page build (unpublished); prospect list of WA TM firms (public sources) | None (drafts only) |
| 1 Substantiate | G5 – G6 | Fill in claims from the G5 benchmark; ToS, privacy and data-handling statement linked from the page; Tara checks the technical copy | G5, G6 |
| 2 Soft launch | G7 pilot | WTGTM pilot; capture reviewer-time and turnaround metrics; draft the case study | G7 |
| 3 Launch | G8 → +90 days | Publish landing page; Owner sends personalised emails (3-touch sequence) to the prospect list; LinkedIn posts (organic, Owner account); Tara referral; offer a free trial check on a historical TMP | G8 + Owner approval of each send |
| 4 Optimise | +90 days | Conversion review, pricing feedback, next segment (LGAs and civil contractors) | — |

**Channels:** Owner email and LinkedIn, landing page with Tally demo form, Tara referral, industry associations (budget TBC, P-23). No paid ads at launch.

**Message hierarchy (draft, subject to P-21 and G5):**
1. Headline: "Professional TMP Checking. Fast. Thorough. Evidence-based." (A-22)
2. Value: "Every finding cites the source, edition and clause. Your accredited reviewer makes the final call."
3. Proof (after G5): processing time; benchmark recall across N documents; reviewed rule count.
4. Safety line, on every asset: "TMP Check is document QA. It does not approve, certify or declare a TMP safe."
5. Offer: $49.95/month platform; $349 single check; 5-pack $1,657.75 ($331.55/check, save 5%); 10-pack $3,141 ($314.10/check, save 10%); credits valid 12 months; ATTG is not registered for GST. Prices come from `config/` at build time.

## 8. Deliverables
| ID | Deliverable | Format | Phase |
|---|---|---|---|
| GTM-01 | Claims and substantiation register | Markdown | 0 |
| GTM-02 | Copy pack (landing page, one-pager, 3-email sequence, 6 LinkedIn posts) | Markdown → DOCX | 0 |
| GTM-03 | Anonymised demo report and annotated sample pages | PDF | 0 (uses historical TMP under A-18; anonymised) |
| GTM-04 | Landing page with Tally demo form | HTML (unpublished until G8) | 0–1 |
| GTM-05 | WA TM prospect list (business contact details from public sources only) | CSV / HubSpot | 0 |
| GTM-06 | WTGTM case study | DOCX/PDF | 2 (WTGTM written consent required) |
| GTM-07 | Launch-performance report | Markdown | 4 |

## 9. Success criteria and quality checklist
- Every claim is traced to GTM-01 with source, date and evidence class. No "approved", "compliant", "safe" or "100%".
- The safety line appears on every customer-facing asset.
- Prices match `config/` exactly. The GST statement is present.
- Tara has reviewed the technical accuracy of the copy (recorded in `docs/reviews/`).
- Landing page: mobile-responsive, accessible (WCAG 2.1 AA contrast), demo form tested end to end, links to ToS and privacy policy.
- Campaign KPIs: O1–O4 above, demo-to-trial ≥ 30% and trial-to-paid ≥ 40% (estimates, to be confirmed after the pilot).

## 10. Approvals required (§3.3)
| ID | Decision | Options | Recommendation | If declined |
|---|---|---|---|---|
| P-21 | Tagline: replace "Comply" (reopens A-22) | A "Check • Cite • Confident"; B "Check • Flag • Fix"; C keep A-22 | A: keeps the alliteration and supports the evidence positioning | R-24 stays High; Owner accepts the claims risk in writing |
| P-22 | Hold all quantitative claims until G5 | A hold; B publish now with sample-size qualifiers | A | Possible misleading-conduct exposure |
| P-23 | Campaign budget | A $0 paid media (time only); B ≤ $500 for an association listing or event | A until G8, then review | No effect on phases 0–2 |
| P-24 | "Every Major confirmed" claim | A remove; B build a rule (one-run Majors downgraded to Query) and test it, then claim | B: it also reduces R-25 and R-28 | Claim removed from all copy |

Nothing is published, sent or bought without the Owner's approval.

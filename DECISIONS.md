# DECISIONS — TMP Check

## Approved
| ID | Decision | Rationale | Date | Authority |
|---|---|---|---|---|
| A-01 | Claude Code appointed sole AI-PM | Handover §1 | 2026-11-20 | Owner |
| A-02 | Subscription $49.95 AUD/month, excludes credits | Handover §3 | 2026-11-20 | Owner |
| A-03 | Credit $149; 10-pack $1,341 (10% off, $134.10 effective) | Handover §3 | 2026-11-20 | Owner |
| A-04 | GST not collected; prices not described as GST-inclusive; configurable | Handover §3 | 2026-11-20 | Owner |
| A-05 | Credit rules 1–9 (upfront, add on payment, 1 per completed check, failures/our errors free, customer re-check charged, 12-month validity, visible ledger, sub billed separately) | Handover §3 | 2026-11-20 | Owner |
| A-06 | Ledger-based credit accounting | Handover §3 | 2026-11-20 | Owner |
| A-07 | Initial jurisdiction WA; 5 check categories; 2 outputs; 5-level severity | Handover §5–8 | 2026-11-20 | Owner |
| A-08 | Human review of 100% of pilot reports | Handover §9, §13 | 2026-11-20 | Owner |
| A-09 | No payment functionality before checking capability validated | Handover §16 | 2026-11-20 | Owner |
| A-10 | Provisional limits: 1 package/check, ≤80 main pages, ≤10 drawing pages | Handover §10 (provisional) | 2026-11-20 | Owner |
| A-48 | **Refunds:** Stripe refunds never remove credits automatically. The webhook flags them; an admin records a negative ledger `adjustment` on the purchase lot (`python -m src.portal.admin adjust`), capped at unused credits, with name and reason. Live payments on hold (A-09) | Owner | 2026-11-25 | Owner |
| A-47 | **Stripe Managed Payments off:** TMP Proof Reader remains merchant of record; Checkout sessions pass `managed_payments[enabled]=false` (`stripe.managed_payments: false`). GST position per A-04 unchanged | Owner | 2026-11-25 | Owner |
| A-46 | **Stripe Option A:** build Payments + Billing integration in Stripe sandbox (test keys) now, on account acct_1UfZfBGdViWULINo "TMP Proof Reader". `payments_enabled: false` and no live keys until G5 (A-09 unchanged). Scope: Starter subscription, single check and 5/10 packs via Checkout, webhooks into the append-only credit ledger | Owner | 2026-11-25 | Owner |
| A-45 | Stripe account approved; Owner opens it. Payment integration still waits for G5 (A-09). Closes the Stripe item of L5 | Owner | 2026-11-25 | Owner |
| A-44 | Portal prices set to A-32 ($349 / $1,657.75 / $3,141.00); A-31 to A-33 supersede A-23's $745 5-pack. Manual credit invoicing (A-23) unchanged | Owner | 2026-11-25 | Owner |
| A-43 | Insurance already obtained by the Owner (L7). Policy details (type, insurer, cover, expiry) to be recorded for G6 | Owner | 2026-11-25 | Owner |
| A-42 | **TMP Draft Builder deferred (partly resolves P-21):** generating draft TMPs from client or tender requirements (MRWA template, approved TGS library, Canva for visual pages) is future development. Trigger: 6 paying customers. Needs before build: a change request, a liability/legal review, an MRWA copyright licence check and G6 data handling. Outline in `docs/requirements/TMP_DRAFT_BUILDER_OUTLINE.md` | Owner | 2026-11-25 | Owner |
| A-41 | **Exception to A-16 (resolves P-22, option B):** full AI-assisted check (passes A–D, two runs) approved for the live TMP BC 016 Bon Marche Arcade Perth only. Owner accepts that the TMP owner's consent has not been obtained and that processing is offshore (R-29). Does not extend to other live TMPs; the A-16/G6 rule still applies | Owner instruction | 2026-11-25 | Owner |
| A-40 | Pilot (G7) price: $145 per check for WTGTM. Resolves P-09 | Owner | 2026-11-25 | Owner |
| A-39 | Credits: if subscription **lapses** (e.g. failed payment) credits are retained and usable on reactivation (12-month expiry still runs); if customer **cancels**, unused credits are forfeited. Resolves P-07 | Owner | 2026-11-25 | Owner |
| A-38 | Offshore AI processing disclosed in Privacy Policy §4 and ToS §6.3; customer consent given by accepting the Terms. Resolves P-08 | Owner | 2026-11-25 | Owner |
| A-37 | Customer documents and reports hosted in an Australian cloud region (e.g. AWS ap-southeast-2 Sydney); provider selection and any spend still need approval. Resolves P-20 | Data residency (L6) | 2026-11-25 | Owner |
| A-36 | Owner approved obtaining quotes (no commitment): legal (Sprintlaw / LegalVision — SaaS ToS + privacy, indicative from ~$1,000+GST per document) and insurance (BizCover / upcover — tech PI avg ~$83–103/mo or from ~$731/yr; cyber from ~$223/yr). Figures from provider websites 2026-11-25, indicative only. Resolves P-19 | Needed for G6 | 2026-11-25 | Owner |
| A-35 | AS 1742.3:2019 purchase ($251.87, official store) deferred to G8. Build proceeds on WA COP + AGTTM (free). Any AS 1742.3-dependent check is raised as Query ('Unable to verify — AS 1742.3 not in rule set'); no AS clause cited. G5 benchmark scored with and without AS-dependent items. Resolves P-06 | Owner; defer spend | 2026-11-25 | Owner |
| A-34 | Launch plan v0.1 approved as working baseline; target 2027-05-17 is provisional and may change via change control (§20.1). Resolves P-18 | Owner | 2026-11-25 | Owner |
| A-33 | Subscription tiers approved: Professional $1,495/mo (5 incl., extra $299); Business $3,995/mo (15 incl., extra $269); Enterprise from $9,990/mo (up to 40); no rollover of unused checks. Single checks and 5/10 packs require Starter $49.95/mo. Resolves P-17 | Per-check ladder below pack rates | 2026-11-25 | Owner |
| A-32 | Base per-check price set at **$349** (5-pack $1,657.75; 10-pack $3,141.00) | Tara: manual check 5+ h | 2026-11-25 | Owner |
| A-31 | Pricing structure v2: tiered subscriptions with included checks + overage; value packs 5 checks −5%, 10 checks −10%. Supersedes $149 list (A-03–A-06). Base per-check price and tier prices still to be set (P-17) | Tara value feedback; margin protection vs unlimited | 2026-11-25 | Owner |
| A-30 | Interstate (QLD/NSW/VIC) references are never acceptable in a WA TMP or in TMP Check output: in-document = Moderate finding; in our wording = blocked to Query | Tara feedback 2026-11-25 (p7 Queensland reference) | 2026-11-25 | Owner (relaying Tara) |
| A-29 | Expenditure approved: up to US$5 Claude API spend for G4 passes A–D on SU_025 | Owner approval in session | 2026-11-25 | Owner |
| A-28 | SU_025_Kanimbla_Road_Nedlands.pdf confirmed as a WTGTM **historical** TMP; may be processed via the Claude API under A-18 | Owner confirmation in session | 2026-11-25 | Owner |
| A-27 | **AI checking runs twice per check** and results are combined (BENCH-04: single run 84–88% recall, two-run union 91%). Est. ≈US$5.40 per 61-page TMP, within the A-16 cap. Configurable 1–3 | Owner approved AI-PM recommendation | 2026-11-20 | Owner |
| A-26 | **Page limit (amends A-10):** one limit of 100 pages per check, drawings included; separate main/drawing caps removed. Trigger: WTGTM SU026 (50 + 11 drawings) rejected under A-10. Still provisional — review with measured AI cost per check | Owner choice of recommended option | 2026-11-20 | Owner |
| A-25 | **Savings card removed (resolves P-16):** no savings figure on the dashboard until G8 commercial validation. Replaced by "Awaiting Review" (drafts with accredited reviewer). Departure from approved mock-up | Owner decision | 2026-11-20 | Owner |
| A-24 | **Credit consumption point (resolves P-15):** 1 credit consumed when the draft report is delivered to the customer's accredited reviewer. Reversal entry if a re-run is needed to correct a TMP Check error (A-05 rule 5). Failed processing consumes nothing | Owner choice of recommended option | 2026-11-20 | Owner |
| A-23 | **Credit purchasing until payments enabled (resolves P-14, P-05):** "Request credits" → manual invoice; admin records ledger purchase after payment received. Five-credit pack offered at $745 (no discount) | Owner choice of recommended option; A-09 retained | 2026-11-20 | Owner |
| A-22 | **Portal wording (resolves P-13):** banner headline "Professional TMP Checking. Fast. Thorough. Evidence-based." Tagline "Check • Comply • Confident" retained | Owner choice of recommended option; CLAUDE.md §2 | 2026-11-20 | Owner |
| A-21 | **Portal sequencing (resolves P-12):** build customer portal stages S1–S4 locally now ($0, no hosting, no live customer data). G4 benchmark remains priority; S5 report screens wait for D-11/D-12. Supersedes S-03 for local build only | Owner choice of recommended option | 2026-11-20 | Owner |
| A-20 | Customer name is **Way to Go Traffic Management** (not 'Way Too Go'). Records corrected; erratum added to PROJECT_HANDOVER.md | Owner confirmation | 2026-11-20 | Owner |
| A-19 | REF-01 proofread report confirmed correct by WTGTM — accepted as reference findings for benchmarking (relayed by Owner) | Owner confirmation | 2026-11-20 | Owner |
| A-18 | WTGTM's **original historical** TMPs, TGSs and proofreading records may be used for development and testing in this Claude Code session (incl. Claude API processing) on WTGTM's **verbal** permission. Amends A-16 for historical documents only; live pilot documents still from G6. Written confirmation recommended but not required. Resolves P-11 (Option C) | Owner decision; speed | 2026-11-20 | Owner |
| A-17 | **Gate 3 signed off (conditional):** 22 core WA rules approved for prototype use on test/anonymised documents (live use from G6). Conditions: Tara's accreditation details (level, number, expiry) and completed review pack filed by **2026-11-27** | Master Prompt §3.3 option A | 2026-11-20 | Owner |
| A-16 | Anthropic Claude API approved as AI processing provider: anonymised/public documents now; live customer documents only after G6 data-handling approval. Budget cap **$150 AUD/month**. Resolves P-04 | Required for proofreading (A) and TMP↔TGS cross-check (D) | 2026-11-20 | Owner |
| A-15 | **Self-approve operating model:** human review is performed by the customer's own accredited person. For WTGTM: Tara (WTGTM, accredited). TMP Check issues a *draft* to the reviewer; the final report + annotated PDF are issued only after the reviewer accepts/edits/rejects every finding. Tara also reviews the initial WA rule set (G3) and sets reference findings (G5). Resolves P-03 | Owner direction; WTGTM retains professional responsibility (Handover §9) | 2026-11-20 | Owner |
| A-14 | WTGTM evidence request v0.2 approved for Owner to send (blank templates raised to Essential) | Critical path G2; Spike S-01 finding | 2026-11-20 | Owner |
| A-13 | **Project baseline approved** (Option A): strategy incl. phased category E (TPR-01), deliverables (DELIVERABLES.md), success criteria (PROJECT_BRIEF.md). Gate 1 signed off. Resolves P-10 | Master Prompt §17 | 2026-11-20 | Owner |
| A-12 | Master Prompt v1.4 adopted as governing framework (resolves P-01) | Owner supplied | 2026-11-20 | Owner |
| A-11 | Project records held in private GitHub repo `abovethetableglobal-au/TMP-Proof-Reader` (resolves P-02) | Persistence beyond ephemeral container | 2026-11-20 | Owner |

## Pending — Owner decision required
| ID | Question | AI-PM recommendation | Needed by |
|---|---|---|---|
| P-21 | Copilot suggests targeting RTM reviewers and/or AI-generated complex TMPs. Change of scope? | No change now. TMP generation deferred by A-42 (trigger: 6 paying customers); RTM-reviewer targeting still open | Post-G6 |

## Provisional assumptions (AI-PM, non-material)
| ID | Assumption | Revisit |
|---|---|---|
| S-05 | Tara's review time is provided by WTGTM at no cost to TMP Check | G6 pilot terms (P-09) |
| S-07 | Tara (WTGTM business owner) holds the WA accreditations needed for all TMP types, incl. RTM for 'complex traffic arrangements' (Code §4.2.3). **Unverified** — Owner's understanding | Verify certificate numbers, levels & expiry before G3 |
| S-06 | Handover §9 "review before release" is met when the accredited reviewer approves the draft before the final report is issued | G6 |
| S-01 | WTGTM TMPs follow MRWA TMP template structure | G2 |
| S-02 | Compliance baseline = WA Code March 2026 + its adopted AGTTM/AS editions (see COMPLIANCE_REGISTER) | G3 |
| S-03 | Prototype is a local pipeline, no web portal until G5 | G5 |
| S-04 | Category E delivered as a core reviewed rule set for pilot, expanded later (sequencing within approved scope; TPR-01) 

## ID reconciliation (2026-11-25, Owner-approved merge of all branches into `main`)
IDs were assigned independently on parallel branches. Portal-line IDs (`claude/fervent-hopper-q3h87z`) were kept, and the others renumbered. Commit messages on the old branches keep the old numbers.
| Branch (old line) | Old ID | New ID |
|---|---|---|
| `g4-postprocess-fixes` | A-21, A-22 | A-28, A-29 |
| `claude/blissful-davinci-884my9` | A-21 … A-31 | A-30 … A-40 |
| `claude/blissful-davinci-884my9` | P-12 … P-15 | P-17 … P-20 |
| `claude/blissful-davinci-884my9` | R-23, R-24 | R-26, R-27 |
| `claude/gallant-gauss-0gunxo` | P-12 | P-21 |
| `claude/gallant-gauss-0gunxo` | R-23 | R-28 |
| `claude/llm-pass-ref-01-src-jys8ll` | BENCH-03, DEF-D03-* | BENCH-06, DEF-L06-* (renumbered before merge) |
Superseded test record: `docs/reviews/BENCH-02_SU026_full_reference.md` (deterministic-only partial run, 2026-11-20) predates the portal-line BENCH-02 and is kept for history.


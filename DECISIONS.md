# DECISIONS — TMP Check

## Approved
| ID | Decision | Rationale | Date | Authority |
|---|---|---|---|---|
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
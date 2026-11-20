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
| P-05 | Five-credit price shown as $745 (no discount). Confirm: is a 5-pack a product, and undiscounted? | Do not offer a 5-pack SKU; customer can buy 5 singles | G8 |
| P-06 | Purchase licensed copy of AS 1742.3:2019 (and possibly AGTTM parts are free from Austroads) | Approve purchase (expected low hundreds AUD — to be quoted) | G3 |
| P-07 | Credit rule gaps: credits on subscription lapse/cancel; refunds; expiry consumption order | Credits retained but unusable while unsubscribed; oldest-first consumption; no cash refunds except our error | G8 |
| P-08 | Data residency: AI processing may occur outside Australia. Acceptable to WTGTM? | Disclose in data-handling statement; obtain WTGTM written consent | G6 |
| P-09 | Pilot commercial terms (free / discounted / full price during pilot) | Discounted pilot credits in exchange for feedback & benchmark data | G6 |

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
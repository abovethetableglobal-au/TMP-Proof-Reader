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
| A-12 | Master Prompt v1.4 adopted as governing framework (resolves P-01) | Owner supplied | 2026-11-20 | Owner |
| A-11 | Project records held in private GitHub repo `abovethetableglobal-au/TMP-Proof-Reader` (resolves P-02) | Persistence beyond ephemeral container | 2026-11-20 | Owner |

## Pending — Owner decision required
| ID | Question | AI-PM recommendation | Needed by |
|---|---|---|---|
| P-03 | Who is the qualified TM professional for (a) compliance rule review and (b) pilot report review, and at what cost? | Engage a WA RCTM/AWTM-accredited reviewer (WTGTM staff or contractor); confirm hourly rate | G2 |
| P-04 | Approve Anthropic Claude API (commercial terms, no training on inputs) as AI processing provider: anonymised docs now, live docs after G6; prototype budget cap | Approve with cap ≈ $150 AUD/month during prototype | Before WS5 |
| P-05 | Five-credit price shown as $745 (no discount). Confirm: is a 5-pack a product, and undiscounted? | Do not offer a 5-pack SKU; customer can buy 5 singles | G8 |
| P-06 | Purchase licensed copy of AS 1742.3:2019 (and possibly AGTTM parts are free from Austroads) | Approve purchase (expected low hundreds AUD — to be quoted) | G3 |
| P-07 | Credit rule gaps: credits on subscription lapse/cancel; refunds; expiry consumption order | Credits retained but unusable while unsubscribed; oldest-first consumption; no cash refunds except our error | G8 |
| P-08 | Data residency: AI processing may occur outside Australia. Acceptable to WTGTM? | Disclose in data-handling statement; obtain WTGTM written consent | G6 |
| P-10 | **Approve project baseline** (Master Prompt §17): strategy incl. phased category E (TPR-01), deliverables (DELIVERABLES.md), success criteria (PROJECT_BRIEF.md) | Approve as presented | G1 |
| P-09 | Pilot commercial terms (free / discounted / full price during pilot) | Discounted pilot credits in exchange for feedback & benchmark data | G6 |

## Provisional assumptions (AI-PM, non-material)
| ID | Assumption | Revisit |
|---|---|---|
| S-01 | WTGTM TMPs follow MRWA TMP template structure | G2 |
| S-02 | Compliance baseline = WA Code March 2026 + its adopted AGTTM/AS editions (see COMPLIANCE_REGISTER) | G3 |
| S-03 | Prototype is a local pipeline, no web portal until G5 | G5 |
| S-04 | Category E delivered as a core reviewed rule set for pilot, expanded later (sequencing within approved scope; TPR-01) | P-10 |

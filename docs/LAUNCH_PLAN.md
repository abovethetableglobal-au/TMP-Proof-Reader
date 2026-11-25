# Launch Plan — TMP Check to live paid service · v0.1 (2026-11-25) · Status: User accepted as working baseline (A-25) — dates provisional, changes via change control

Tier: Significant. Review: simulated three-perspective (§5.3). Target live launch: **2027-05-17** (after G8), soft launch to WTGTM from G7.

## 1. Where we are (verified fact)
| Gate | Status |
|---|---|
| G1 Initiation | User accepted |
| G2 Customer requirements | In progress (1 of ≥5 evidence packages analysed) |
| G3 Compliance framework | User accepted — conditional (22 approved rules + 2 drafts; target 30–60) |
| G4 Prototype | In progress — checks coded; report/annotated-PDF generator and API run outstanding |
| G5–G8 | Not started |
| Pricing | Approved (A-22–A-24) |

## 2. Three-perspective review (simulated)
| Perspective | Key point |
|---|---|
| Product/technical lead | Accuracy is the product. Do not launch before G5 shows recall ≥ agreed target with 0 unsupported Critical findings. A portal + payments is ~4–6 weeks of build. |
| Legal/risk (WA TM industry) | Need: Terms of Service limiting liability (QA, not approval), privacy policy (APP compliance), data-handling statement incl. offshore AI processing (P-08), Professional Indemnity insurance. |
| Commercial/go-to-market | $349 is supported by Tara's 5+ h estimate but untested with non-WTGTM buyers. Pilot converts WTGTM first; then 5–10 WA TM companies via direct outreach and Tara referral. |
Consolidated: launch is gated on accuracy (G5) and legal/insurance (G6), not on code. Run the legal and commercial tracks in parallel now.

## 3. Launch workstreams
| # | Workstream | Key deliverables | Owner | Due | Depends on |
|---|---|---|---|---|---|
| L1 | Engine completion (G4) | Report PDF + annotated PDF generator; TGS index; first full API run on REF-01 | AI-PM | 2026-12-18 | API key in session |
| L2 | Evidence & benchmark (G2, G5) | ≥5 WTGTM packages; Tara blind reference findings; accuracy in TEST_REGISTER | Owner/Tara/AI-PM | 2027-02-26 | WTGTM files |
| L3 | Rule library to 30–60 (G3 close) | WA COP + AGTTM rules; Tara review. AS 1742.3 rules added at G8 (A-26) | AI-PM/Tara | 2027-01-29 | — |
| L4 | Customer portal (MVP) | Login, upload, credit balance, draft→reviewer disposition→final, download | AI-PM | 2027-03-05 | Hosting decision |
| L5 | Payments & ledger | Stripe subscriptions + packs, append-only ledger, invoices | AI-PM | 2027-03-05 | Stripe account; GST decision |
| L6 | Security & data handling (G6) | AU-hosted storage, encryption, retention/deletion, access logs, data-handling statement, WTGTM written consent | AI-PM/Owner | 2027-03-12 | P-08 |
| L7 | Legal & insurance (G6) | ToS, privacy policy, PI + cyber insurance quotes, ABN/business name check | Owner (lawyer/broker) | 2027-03-12 | Spend approval |
| L8 | Pilot (G7) | 10–20 live WTGTM TMPs under review; turnaround and reviewer-time metrics | WTGTM/AI-PM | 2027-04-23 | G6 |
| L9 | Go-to-market (G8) | Website/landing page, demo report (anonymised), case study with WTGTM, outreach list of WA TM firms | AI-PM drafts; Owner sends | 2027-05-14 | Pilot results |
| L10 | Operations | Support SOP, incident process, rule-update monitoring (MRWA quarterly) | AI-PM | 2027-05-14 | — |

## 4. Launch acceptance criteria (go/no-go)
- G5 benchmark recall and precision meet agreed targets; 0 unsupported Critical findings released.
- G6 SOPs, ToS, privacy policy, data-handling statement approved; PI insurance bound.
- Pilot: ≥10 live TMPs, reviewer time ≤ 2 h median, WTGTM acceptance.
- Payments tested end-to-end (purchase, consume, failed check = no charge, expiry).
- AS 1742.3:2019 purchased, AS rules added and benchmark re-run (A-26).
- Owner sign-off on G8.

## 5. Budget (estimates — not approved)
| Item | Estimate (AUD) |
|---|---|
| AI processing | ≤ $150/month (approved cap A-16) |
| Hosting (AU region) + domain | $30–100/month |
| AS 1742.3:2019 licence (at G8, A-26) | $251.87 |
| Legal: ToS + privacy | $1,500–4,000 one-off |
| PI + cyber insurance | $1,500–4,000/year |
| Stripe | per-transaction fees only |

## 6. Approvals required (§3.3)
| ID | Decision | Recommendation | If declined |
|---|---|---|---|
| P-13 | Approve this launch plan and target date 2027-05-17 | Approve | Plan stays draft; gates continue as is |
| P-14 | Engage lawyer for ToS/privacy and broker for PI/cyber quotes | Approve quotes only (no commitment) | Cannot pass G6 |
| P-15 | Hosting: Australian-region cloud (e.g. AWS Sydney) | Approve | Data residency risk for customers |
| P-08 | Offshore AI processing disclosure + WTGTM written consent | Approve | No live documents → no pilot |

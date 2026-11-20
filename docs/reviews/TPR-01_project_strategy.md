# TPR-01 — Three-Perspective Review: Project Strategy & Baseline

| Field | Value |
|---|---|
| Date | 2026-11-20 |
| Subject | Initial strategy, plan, architecture and success criteria (Gate 1 baseline) |
| Method | **Simulated** expert perspectives (single AI model — Claude Code). Not independent. Independent review requested via IR-01 (human-mediated). |
| Status | Ready for user review |

## Perspectives selected
| # | Perspective | Why |
|---|---|---|
| P1 | WA traffic management compliance practitioner (RTM/AWTM-level) | Domain correctness; safety; what WTGTM actually needs checked |
| P2 | Solution architect (document AI) | Feasibility of extraction, drawings, annotation, evidence validation |
| P3 | Commercial analyst (SMB SaaS / professional services) | Unit economics, pricing, pilot design, scalability |

## P1 — TM compliance practitioner
- **Observations:** The outsourced proofreader at $45/hr was most likely doing categories A–C (editorial, consistency, completeness) plus some D. Category E (compliance) is the highest-liability, lowest-maturity area and depends on a reviewed rule library that does not yet exist.
- **Risks:** Mis-citing AGTTM edition (WA uses Ed 1.1 for most parts); treating AGTTM guidance ("should") as mandatory; checking generic TMPs against site-specific requirements.
- **Recommendation:** Deliver E as a small, reviewed rule set first — WA Code §4.2 TMP content, §3.5 authorisation, §8 accreditation — and expand by evidence from rejected TMPs (WTGTM item A7). Applicability conditions (state vs LGA road, generic vs site-specific) must be captured before any rule fires.

## P2 — Solution architect
- **Observations:** Text-layer TMPs (from Word templates) are tractable. TGS drawings are the main technical unknown: vector PDF from CAD/TGS software is workable; scanned/raster drawings are much weaker.
- **Risks:** LLM findings without verifiable evidence; annotation coordinates drifting from cited text; OCR noise generating false proofreading findings.
- **Recommendation:** Evidence validator is mandatory (every finding must quote text located on the cited page, or become a Query). Run an early technical spike on the **public MRWA TMP template** to prove extraction + annotation before customer documents arrive. Capture drawing format in the evidence request (already item B9).

## P3 — Commercial analyst
- **Observations:** Customer value case is strong ($405 → $149/$134.10). The weak point is **our** cost: mandatory human review during the pilot. If the reviewer is the Owner, the model does not scale (R-15); if a paid TM professional, review must be ≲45 min to retain margin (R-03).
- **Risks:** Unknown WTGTM volume; pilot priced at zero creates no willingness-to-pay signal.
- **Recommendation:** Measure review minutes from the very first prototype run and treat "review time per check" as a primary engineering KPI, not an afterthought. Pilot should be paid (discounted), not free, to test willingness to pay.

## Constructive challenge
| Issue | P1 | P2 | P3 | Resolution |
|---|---|---|---|---|
| Scope of E at pilot | Narrow, reviewed | Narrow reduces build risk | Narrow is fine if A–D deliver value | **Agreed:** phase E — core rule set for pilot, expand later. Within approved scope (sequencing, not a scope change). |
| Start building before evidence? | Not on compliance | Yes — technical spike on public template | Yes, cheap de-risking | **Agreed:** spike on public material only; no checking-engine tuning until real documents arrive. |
| Who reviews | Must be accredited | — | Cost & scalability | **Unresolved → Owner decision P-03.** |
| Free vs paid pilot | — | — | Paid (discounted) | **Owner decision P-09.** Minority note: a free first 2–3 checks may be needed to secure participation. |

## Consolidated recommendation
1. Proceed with the plan as baselined, with **category E phased**: pilot uses a core reviewed WA rule set; expansion driven by WTGTM rejection evidence.
2. Begin a technical spike now on public MRWA templates (extraction, annotation, evidence validation) — no customer data, no spend.
3. Make **review time per check** a tracked KPI from the first run.
4. Appoint an accredited reviewer early (P-03) — it gates G3, G5 and the pilot.
5. Obtain independent review of this strategy (IR-01).

# PROJECT_PLAN — TMP Check

Baseline: 2026-11-20. Dates are **targets**, driven mainly by WTGTM evidence turnaround and reviewer availability. Australian Dec–Jan holiday shutdown is built in.

## Critical path
`WTGTM evidence (WS2)` → `Reference findings by qualified reviewer (WS10)` → `Prototype (WS5–7)` → `Benchmark (Gate 5)` → `Security/SOPs (WS8)` → `Pilot (WS11)` → `Commercial (WS9, WS12)`

Compliance library (WS3) runs in parallel with WS2 and must be reviewed before Gate 3.

## Gates
| Gate | Criteria | Target | Status |
|---|---|---|---|
| G1 Initiation | Records, scope, plan established; Owner sign-off | 2026-11-27 | **User accepted 2026-11-20** (A-13) |
| G2 Customer requirements | ≥5 representative TMP packages + proofreader corrections received and analysed; requirements doc approved | 2026-12-18 | Blocked (WTGTM evidence) |
| G3 Compliance framework | Initial WA rule set (target 30–60 rules) verified against primary sources and reviewed by qualified TM professional | 2027-01-29 | **Awaiting approval** (22 core rules reviewed; reviewer accreditation details outstanding) |
| G4 Working prototype | Representative TMP processed → report PDF + annotated PDF | 2027-02-05 | Not started |
| G5 Benchmark | Results vs independently reviewed findings; accuracy recorded in TEST_REGISTER | 2027-02-26 | Not started |
| G6 Pilot readiness | Security, data-handling, human-review SOPs approved by Owner (and WTGTM where needed) | 2027-03-12 | Not started |
| G7 Controlled pilot | Agreed number of live TMPs processed under human review | 2027-03-15 → 2027-04-23 | Not started |
| G8 Commercial readiness | Economics, pricing, acceptance validated | 2027-05-14 | Not started |

## Workstreams
| WS | Workstream | Owner | Depends on | Next action | Status |
|---|---|---|---|---|---|
| 1 | Project management | AI-PM | — | Maintain records; manage G2 | In progress |
| 2 | Customer discovery | AI-PM (Owner sends) | Owner approval of request | Owner sends request (approved A-14); AI-PM tracks responses | Awaiting input |
| 3 | Regulatory research | AI-PM; Tara (WTGTM reviewer) | AS 1742.3 access (P-06) | Build source register → draft rules from Code §4.2 (core set per TPR-01) | In progress |
| 4 | Product design | AI-PM | WS2 | Customer + reviewer workflow wireframes | Not started |
| 5 | Checking engine | AI-PM | WS2, WS3, P-04 | Prompt/rule design on anonymised samples | Not started |
| 6 | Document processing | AI-PM | Sample documents | Technical spike on public MRWA TMP template | Not started |
| 7 | Report generation | AI-PM | WS5 | Report template + annotation spike | Not started |
| 8 | Security | AI-PM; Owner approves | P-04, P-08 | Draft data-handling statement | Not started |
| 9 | Commercial system | AI-PM | **G5 passed** | Ledger design only (no payments yet) | Not started |
| 10 | Testing | AI-PM; Tara (blind reference findings) | WS2 | Build reference set | Awaiting input |
| 11 | Pilot | AI-PM; Owner; WTGTM | G6 | Pilot agreement terms | Not started |
| 12 | Commercial launch | Owner; AI-PM | G8 | — | Not started |

## Budget (Master Prompt §11.1)
| Item | Approved | Committed | Actual |
|---|---|---|---|
| Project budget | $150 AUD/month (Claude API only) | $0 | $0 cash |
| Firecrawl research credits (Owner's account) | Within existing tools | — | ~180 credits (2026-11-20) |
| Claude API (A-16) | **$150 AUD/month cap** | $0 | $0 |
| Requested: AS 1742.3:2019 licence (P-06) | Pending | — | — |
| Requested: TM reviewer fees (P-03) | Pending | — | — |

## Immediate priorities (next 10 working days)
1. Owner: approve & send WTGTM evidence request (WS2).
2. Owner: decide P-01…P-04 (DECISIONS.md).
3. AI-PM: complete WA source register; draft core rule set (Code §3.5, §4.2, §8) — status draft-unverified (TPR-01).
4. AI-PM: extraction/annotation/evidence-validation spike using **public** MRWA TMP template (no customer data, no spend).
6. Owner: transfer IR-01 independent review to ChatGPT or Gemini.
5. AI-PM: data-handling statement draft (WS8) for Owner/WTGTM.

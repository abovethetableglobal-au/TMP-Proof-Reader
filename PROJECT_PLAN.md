# PROJECT_PLAN — TMP Check

Baseline: 2026-11-20. Dates are **targets**, driven mainly by WTGTM evidence turnaround and reviewer availability. Australian Dec–Jan holiday shutdown is built in.

## Critical path
`WTGTM evidence (WS2)` → `Reference findings by qualified reviewer (WS10)` → `Prototype (WS5–7)` → `Benchmark (Gate 5)` → `Security/SOPs (WS8)` → `Pilot (WS11)` → `Commercial (WS9, WS12)`

Compliance library (WS3) runs in parallel with WS2 and must be reviewed before Gate 3.

## Gates
| Gate | Criteria | Target | Status |
|---|---|---|---|
| G1 Initiation | Records, scope, plan established; Owner sign-off | 2026-11-27 | **Records complete — awaiting Owner sign-off** |
| G2 Customer requirements | ≥5 representative TMP packages + proofreader corrections received and analysed; requirements doc approved | 2026-12-18 | Not started (blocked: evidence request) |
| G3 Compliance framework | Initial WA rule set (target 30–60 rules) verified against primary sources and reviewed by qualified TM professional | 2027-01-29 | In progress (source register started) |
| G4 Working prototype | Representative TMP processed → report PDF + annotated PDF | 2027-02-05 | Not started |
| G5 Benchmark | Results vs independently reviewed findings; accuracy recorded in TEST_REGISTER | 2027-02-26 | Not started |
| G6 Pilot readiness | Security, data-handling, human-review SOPs approved by Owner (and WTGTM where needed) | 2027-03-12 | Not started |
| G7 Controlled pilot | Agreed number of live TMPs processed under human review | 2027-03-15 → 2027-04-23 | Not started |
| G8 Commercial readiness | Economics, pricing, acceptance validated | 2027-05-14 | Not started |

## Workstreams
| WS | Workstream | Owner | Depends on | Next action | Status |
|---|---|---|---|---|---|
| 1 | Project management | AI-PM | — | Owner sign-off of G1 | Active |
| 2 | Customer discovery | AI-PM (Owner sends) | Owner approval of request | Owner sends `docs/WTGTM_EVIDENCE_REQUEST.md` | Ready |
| 3 | Regulatory research | AI-PM; Qualified reviewer | Reviewer appointed (P-03); AS 1742.3 access (P-06) | Build source register → draft rules from Code §4.2 | Active |
| 4 | Product design | AI-PM | WS2 | Customer + reviewer workflow wireframes | Not started |
| 5 | Checking engine | AI-PM | WS2, WS3, P-04 | Prompt/rule design on anonymised samples | Not started |
| 6 | Document processing | AI-PM | Sample documents | Extraction/OCR spike on real document formats | Not started |
| 7 | Report generation | AI-PM | WS5 | Report template + annotation spike | Not started |
| 8 | Security | AI-PM; Owner approves | P-04, P-08 | Draft data-handling statement | Not started |
| 9 | Commercial system | AI-PM | **G5 passed** | Ledger design only (no payments yet) | Deferred |
| 10 | Testing | AI-PM; Qualified reviewer | WS2, P-03 | Methodology done; build reference set | Methodology drafted |
| 11 | Pilot | AI-PM; Owner; WTGTM | G6 | Pilot agreement terms | Not started |
| 12 | Commercial launch | Owner; AI-PM | G8 | — | Not started |

## Immediate priorities (next 10 working days)
1. Owner: approve & send WTGTM evidence request (WS2).
2. Owner: decide P-01…P-04 (DECISIONS.md).
3. AI-PM: complete WA source register; draft first rule set from Code §4.2 (TMP content) — status DRAFT-UNVERIFIED.
4. AI-PM: extraction/annotation spike using **public** MRWA TMP template (no customer data).
5. AI-PM: data-handling statement draft (WS8) for Owner/WTGTM.

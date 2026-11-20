# Customer Portal Dashboard — Implementation Plan (v0.1, PROPOSED)

| Field | Value |
|---|---|
| Deliverable | D-17 |
| Source brief | Owner "TMP Check – Dashboard UI Implementation Brief" + dashboard mock-up, received 2026-11-20 |
| Status | In progress — all decisions resolved (A-21–A-25); S1 complete |
| Process tier | Significant (§2A) |
| Review | Simulated three-perspective review (§5.3) — §7 below |

## 1. Repository review (brief §8 steps 1–4)

| Item | Finding | Evidence class |
|---|---|---|
| Framework | None for web. Python 3.11 local pipeline only (`src/tmpcheck/`). No UI, DB, auth or ledger code exists | Verified fact |
| Reusable | `det_checks.py`, `template_diff.py`, `llm_checks.py` (Finding model with 5-level severity + evidence validation), 22 YAML rules in `compliance/rules/` (feeds Compliance Library page) | Verified fact |
| Missing for portal | Report PDF (D-11), annotated PDF (D-12), reviewer disposition workflow, ledger, auth, storage | Verified fact |
| Planned stack | ARCHITECTURE.md Stage 2: FastAPI + HTMX or Next.js; Supabase (Sydney) or AWS ap-southeast-2; Postgres append-only ledger | Verified fact (proposed, approved as D-05) |
| Gate position | G4 in progress (LLM passes awaiting API key run); portal planned for G6 (S-03, ARCHITECTURE Stage 2) | Verified fact |

## 2. Conflicts with approved requirements (§6.2) — must be resolved before build

| # | Brief item | Conflicts with | Recommendation | Decision |
|---|---|---|---|---|
| C-1 | Build data-connected portal now | S-03 (no portal until G5), R-14 over-building, CLAUDE.md §5 "build only what the current gate needs"; G4 engine still unproven | Build portal **locally in parallel** (no hosting, no spend, no live customer data) but keep G4 benchmark as priority | **P-12** |
| C-2 | Headline "Fast. Accurate. **Compliant.**" | CLAUDE.md §2 (never output "compliant"); Handover §7, §9; R-16. "Accurate" is unproven until G5 | "Professional TMP Checking. Fast. Thorough. Evidence-based." | **P-13** |
| C-3 | Tagline "Check • **Comply** • Confident" | Lower risk (verb directed at customer), but implies compliance outcome | Retain only with Owner acceptance; alternative "Check • Cite • Confident" | **P-13** |
| C-4 | Buy More Credits / Purchase a Credit Pack | A-09, CLAUDE.md §5: no payments before G5; Stripe planned post-G8 | Buttons open "Request credits" (manual invoice). Owner/admin records purchase in ledger after payment received | **P-14** |
| C-5 | Five-credit pack $745 listed as approved | P-05 pending (AI-PM recommended no 5-pack SKU) | Treat brief as Owner resolving P-05: 5-pack offered at $745, no discount | Confirm with P-14 |
| C-6 | Recent Checks status "Completed" | A-15 / CLAUDE.md §2: drafts only until reviewer dispositions every finding | Statuses: Uploaded · Processing · Draft — awaiting reviewer · Final issued · Failed (no credit) | Applied (safety gate, not optional) |
| C-7 | "No Issues Found" in findings column | Handover §7 wording | "No issue identified in this check" | Applied |
| C-8 | Credit consumed on "successfully completed check" — point of consumption undefined | A-05 rule 3 | Consume when draft is successfully delivered to reviewer; reversal entry if TMP Check error (rule 5) | **P-15** |
| C-9 | Potential Savings card | COMMERCIAL_MODEL benchmark is an assumption ($405/check), not verified customer data | Hide until Owner sets a per-customer baseline; then show Σ(baseline − credit price) for **final-issued** checks, labelled "estimate" | **P-16** |
| C-10 | Mock-up org name "Way Too Go" | A-20 ("Way to Go") | Org name comes from account record only | Applied |

## 3. Recommended stack (lowest cost, $0 until G6)

| Layer | Choice | Rationale |
|---|---|---|
| Web | FastAPI + Jinja2 templates + HTMX | Same language as pipeline; no JS build chain; listed in D-05 |
| Styling | Hand-written CSS with design tokens (navy / white / safety orange) | No framework licence or build step; matches mock-up exactly |
| DB | SQLite (local) → Postgres at G6 via SQLAlchemy | Zero cost now; portable |
| Auth | Session cookies + argon2 password hashes; roles `customer_user`, `customer_reviewer`, `admin` | Replaced/fronted by Supabase Auth at G6 if chosen |
| Storage | Local `customer-docs/<org_id>/<check_id>/` (git-ignored) → private bucket at G6 | Per-org prefix = tenant separation |
| Jobs | In-process background task → worker at G6 | Pipeline runs async |
| Banner image | Licence-free photo or commissioned/AI-generated image; no paid stock | No spend without approval |

## 4. Data model (minimum)

| Table | Key columns | Notes |
|---|---|---|
| `organisation` | id, name, subscription_status, subscription_started_at | Status entered by admin until Stripe |
| `user` | id, org_id, email, password_hash, role | |
| `check` | id, org_id, doc_ref, filename, status, created_at, completed_at, failure_reason, credit_lot_id | Status enum per C-6 |
| `finding` | id, check_id, severity, page, section, evidence, disposition{pending, accepted, edited, rejected} | From `llm_checks.Finding` |
| `credit_ledger` | per COMMERCIAL_MODEL (append-only) | Balance and expiry derived, never stored |
| `audit_event` | id, org_id, user_id, action, object, at | Every view/download/upload |
| config | prices, GST flag | YAML, not code literals (CLAUDE.md §5) |

## 5. Staged delivery

| Stage | Scope | Depends on | Done when |
|---|---|---|---|
| S1 Shell ✅ (D-18) | Layout, nav, header, banner, footer, responsive (desktop/tablet/mobile), design tokens, all empty states | P-12, P-13 | Visual match to mock-up at 1440/1024/390 px; no illustrative data |
| S2 Accounts | Login, org separation, roles, audit log | S1 | Cross-tenant access tests fail closed |
| S3 Ledger | Credit ledger, balance, expiry, history, admin "record purchase" | P-14, P-15 | Ledger unit tests: purchase/consume/reversal/expiry/oldest-first |
| S4 Upload → check | Drag-drop, type/size validation (PDF/DOCX ≤ 20 MB, page limits A-10), progress, pipeline job, failure → no credit | S2, S3 | Corrupt/oversize/wrong-type rejected with message; failure creates no consume row |
| S5 My Checks + review | Check list, findings, reviewer disposition, draft→final, report/annotated downloads | D-11, D-12 | Final cannot be issued with any pending finding |
| S6 Library + Help | 22 rules (source, edition, clause, verification date), FAQ, contact | — | Every rule shows source + edition + clause |
| S7 QA | Playwright screenshots, accessibility (WCAG 2.1 AA contrast), security review | S1–S6 | Brief §9 criteria all evidenced |

## 6. Brief §9 acceptance mapping

| Criterion | Stage |
|---|---|
| Reflects reference, consistent branding, navigation | S1 |
| Upload connected to checking workflow | S4 |
| Account/subscription accurate; credits from ledger; pricing correct | S3 + config |
| No illustrative data; recent checks real | S1–S5 (empty states) |
| Desktop/tablet/mobile | S1, S7 |
| Security & tenant separation | S2, S7 |
| Empty/error states | S1, S4 |

## 7. Three-perspective review (simulated, §5.3)

| Perspective | Key point | Resolution |
|---|---|---|
| Solution architect | Portal before engine validation risks rework (report/annotation formats unknown) | Build S1–S4 now; S5 waits for D-11/D-12 |
| Product/UX | Mock-up is strong; "Completed" + "No Issues Found" mislead customers about review status | C-6, C-7 applied |
| Security / regulatory | "Compliant" headline creates liability (R-09, R-16); multi-tenant isolation needs tests from day one | C-2 escalated; S2 tests mandatory |

Consolidated recommendation: approve P-12 Option "build locally in parallel", adopt C-2 wording, defer purchase to manual-invoice flow.

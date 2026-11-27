# CR-01 — Managed service: Operator Console, daily intake and billing

| Field | Value |
|---|---|
| Raised | 2026-11-27 by Owner |
| Type | Material change (Master Prompt §20.1) — operating model and scope |
| Status | Awaiting approval |
| Review | Simulated three-perspective review (one AI model) — §5.3 |

## 1. Requested change
The Owner hosts and runs TMP Check as a **managed service**. Customers (e.g. WTGTM/Tara, Blackstone) submit TMPs to a Google Drive / mailbox. A **daily sweep at 12:30** collects them; TMPs captured are processed and returned **the same day**; anything received after 12:30 goes in the **next business day's** sweep. The Owner needs a **dashboard** to record customers, run their checks, track work, and apply credits. Intent: build a business that can be **sold**.

## 2. Answer to "Is it a customer billing platform I need?"
**No — recommendation:** an **Operator Console** (back office) inside the existing portal, with billing handled by existing services:

| Need | Build or buy | Why |
|---|---|---|
| Customers, contacts, reviewers, Drive folders, pricing plan | **Build** (Operator Console) | Core to the service; already half-modelled (organisations, users) |
| Credits (grant, adjust, expiry, statement) | **Build** — already exists as an append-only ledger; add screens | Ledger is the auditable source of truth (A-06) |
| Work queue, due dates, turnaround tracking | **Build** | Unique to this service |
| Taking payment, invoices, receipts | **Buy — Stripe** (already in sandbox, A-46) | Don't build a billing platform; Stripe Invoicing handles cards, bank transfer, receipts |
| Bookkeeping, GST, BAS | **Buy — Xero/MYOB** | Accountant-ready books matter for a sale |

## 3. Proposed scope (phased)
| Phase | Delivers | Depends on |
|---|---|---|
| **1. Operator Console** | Customer list and record (legal name, ABN, billing contact, reviewers + accreditation, plan, status); credits screen (grant, adjust with reason, ledger view, statement); **work queue** (today's batch, due time, status, AI cost, overdue flag); run a check on a customer's behalf (upload as operator) | Approval only |
| **2. Daily intake & return** | Scheduled sweep 12:30 AWST Mon–Fri excluding WA public holidays; per-customer intake folder; files matched to customer, validated, queued with due date; unreadable files flagged (no credit); outputs returned to the customer's "Returned" folder + email notice | Intake channel decision; Google Drive access (data-handling approval, G6) |
| **3. Billing & business metrics** | Stripe invoices from the console (credit packs, subscriptions, monthly usage); export to Xero; metrics: checks/month, revenue, AI cost/check, on-time %, per-customer usage | Stripe live (after G5), Xero connection |

**Turnaround rule (as stated by Owner):** received by 12:30 on a business day → returned that day; after 12:30 or non-business day → next business day's 12:30 batch, returned that day.

## 4. Three-perspective review (simulated)
| Perspective | Key point | Recommendation |
|---|---|---|
| Operations manager | A fixed daily cut-off makes workload and promises predictable; the risk is one person (Owner) as single point of failure for review and release | Console must show what is due, overdue and blocked at a glance; record who did what |
| Commercial / M&A analyst | Buyers value recurring revenue, documented customers and contracts, clean books and processes that don't depend on the founder | Keep customer, credit and job records in the system (not email/spreadsheets); use Stripe + Xero; document SOPs |
| Security & compliance | Customer TMPs move through Google Drive and a mailbox — new places confidential data lives; same-day promise conflicts with draft Terms ("turnaround is an estimate") | Approve Drive/mailbox in the data-handling statement before live use; align Terms with the 12:30 rule; per-customer folders with restricted sharing |

**Consolidated:** build Phase 1 now (no new data risk, uses existing ledger), Phase 2 after the intake channel and data-handling are settled, Phase 3 at G5.

## 5. Impact
| Area | Impact |
|---|---|
| Scope | Adds operator console and automated intake; customer portal self-upload remains available |
| A-15 self-approve model | **Needs confirming:** does the customer's accredited reviewer still approve each report in the portal, or do you return final reports directly? |
| Cost | Phase 1–2: no new paid services (Google Drive under existing account); AI cost unchanged per check |
| Timeline | Phase 1 is a few build sessions; Phase 2 depends on decisions below |
| Risk | New: Drive/mailbox data exposure; single-operator dependency; same-day commitment |

## 6. Decisions needed (one at a time)
1. **Intake channel:** one shared Google Drive folder per customer, or one mailbox that customers email TMPs to (attachments saved to Drive)?
2. Review model under the managed service (keep A-15 customer approval, or Owner-run review?).
3. Turnaround promise wording in the Terms (guarantee vs target).
4. Approve Google Drive/mailbox in the data-handling statement.

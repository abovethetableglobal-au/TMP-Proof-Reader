# Architecture — Lowest-Cost Practical Path (v0.1, PROPOSED)

Principle: prove the checking engine with near-zero infrastructure, then add the portal and payments only after Gate 5.

## Stage 1 — Prototype (G4–G5): local pipeline, no web app
```
input/ (TMP + TGS PDFs/DOCX)
  → intake: validate type/size/pages, malware scan (ClamAV), DOCX→PDF (LibreOffice headless)
  → extract: PyMuPDF text+layout per page; OCR via ocrmypdf/Tesseract where no text layer
  → structure: headings, sections, tables, page map; project-fact sheet (names, roads, dates, stages, drawing refs)
  → checks:
       A proofreading      — LLM pass per section (+ AU-English dictionary)
       B consistency       — deterministic fact comparison across pages + LLM
       C completeness      — template/rule-driven presence checks
       D TMP↔TGS cross-check — drawing text extraction + LLM vision; low-confidence → Query
       E compliance        — only rules with status ≥ verified; must cite rule_id
  → evidence validator: every finding must quote text that exists on the cited page; else dropped or → Query
  → review sheet (HTML) for human reviewer: accept / edit / reject each finding; timer captured
  → outputs: Report PDF (HTML→PDF, WeasyPrint) + Annotated PDF (PyMuPDF highlights + numbered notes on a copy)
```
| Component | Choice | Cost |
|---|---|---|
| Language | Python 3.11 | $0 |
| PDF/annotation | PyMuPDF | $0 for prototype; AGPL — confirm licensing obligations for hosted use before G6 (alternatives: pypdf + pdfplumber) |
| OCR | ocrmypdf + Tesseract | $0 |
| LLM | Anthropic Claude API (P-04) | Pay per use, est. $2–15/check |
| Rules | YAML in git | $0 |

## Stage 2 — Pilot (G6–G7): minimal portal
| Need | Proposal | Indicative cost |
|---|---|---|
| Auth, DB, private storage | Supabase (Sydney region) or AWS ap-southeast-2 | $0–40/month |
| Web app | Single small app (e.g. Next.js or FastAPI + HTMX) | Hosting $0–25/month |
| Processing | Background worker running the Stage 1 pipeline | Included / small VM |
| Review | Admin review screen (Stage 1 sheet, productised) | — |
| Ledger | Postgres append-only table (see COMMERCIAL_MODEL) | — |
| Audit log | Append-only events table | — |

## Stage 3 — Commercial (post-G8)
Stripe Billing (AUD subscriptions + one-off credit packs, webhooks → ledger). Pilot can run on manual invoicing to avoid premature build (A-09).

## Security baseline
TLS everywhere; encryption at rest (provider-managed); per-customer storage prefixes + row-level security; signed short-lived download URLs; retention default 90 days post-delivery (Owner to confirm); AI provider configured for no training use; audit log of every access.

## Open technical questions
1. Drawing formats from WTGTM (vector PDF vs scanned) — determines D-category approach.
2. PyMuPDF licensing for SaaS use.
3. AI processing region / zero-data-retention availability (P-08).

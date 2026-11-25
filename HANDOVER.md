# HANDOVER — TMP Check (current state)

_Last updated: 2026-11-25 by AI-PM — short-form restart notes: `handovers/attg.md`_

## Current state
| Gate | Status |
|---|---|
| G1 Initiation | User accepted (A-13) |
| G2 Customer requirements | In progress — REF-01 report + source TMP received; analysis 01 done |
| G3 Compliance framework | User accepted, conditional (A-17) — Tara accreditation details + review pack due 2026-11-27 |
| G4 Working prototype | In progress — deterministic checks done; LLM passes coded; API key added (loads in a new session) |
| G4 Working prototype | In progress — deterministic checks done (10/110 vs REF-01, BENCH-02); LLM passes coded; scorer built; awaiting API key in container |

## Repository
Private: https://github.com/abovethetableglobal-au/TMP-Proof-Reader (branch `main`). Cloud environment: **TMP-Proof-Reader** (personal).

## Code
| Module | Purpose |
|---|---|
| `src/tmpcheck/template_diff.py` | Missing Main Roads template headings (rule WA-COP-4.2.1-001) |
| `src/tmpcheck/det_checks.py` | Placeholders, jurisdiction wording, missing headers, repeated sentences (no LLM) |
| `src/tmpcheck/llm_checks.py` | Claude API passes A–D, structured findings, evidence validation, cost logging |
| `src/tmpcheck/score.py` | Scores findings vs reference JSON (auto-match + adjudication) |
| `src/spike/completeness_spike.py` | Spike S-01 (annotation prototype) |
| `compliance/rules/*.yaml` | 22 approved WA rules |

## Session 2026-11-24 — status
- **Blocked:** `ANTHROPIC_API_KEY` not set. Anthropic hosts can't use network secrets; Owner must add it as an environment variable (env menu → Edit), then start a new session.
- **Blocked:** source PDFs not re-uploaded (step 2).
- **Received (not stored in Git):** two TMP Check outputs (5-pp report "FINAL", 15-pp annotated DRAFT) generated outside this repo, run on a TMP Check DRAFT report, not the TMP. Issues found: FINAL issued with placeholder reviewer "Your Name" (breaks the A-15 gate); "TEST UPDATE" reviewer note; duplicate findings; unlocated quotes not downgraded to Query; category E unlabelled; conflicting actions (F-007); evidence not matching the finding (F-008); truncated list (F-013).
- **Open question to Owner:** which tool/platform produced those PDFs?

## Next session — exact steps
Branch `g4-postprocess-fixes` holds review-defect fixes D1–D5 (`src/tmpcheck/postprocess.py`); check it out.
Owner approved up to US$5 for passes A–D on SU_025 (A-29). SU_025 is historical (A-28).
1. Confirm key: `python3 -c "import os;print(bool(os.environ.get('ANTHROPIC_API_KEY')))"` → `True`.
2. Owner re-uploads `SU_025_Kanimbla_Road_Nedlands.pdf`; copy to `customer-docs/wtgtm-2026-11-20/` (git-ignored).
3. Run: `python3 -m src.tmpcheck.llm_checks customer-docs/wtgtm-2026-11-20/SU_025_Kanimbla_Road_Nedlands.pdf customer-docs/wtgtm-2026-11-20/out/llm.json` — stop if a pass exceeds US$2.
4. Log cost per pass in COMMERCIAL_MODEL.md and PROJECT_LOG.md.
5. Deterministic baseline on SU_025 (2026-11-25): PH-TBA 4, PH-ANGLE 3, JX-MRWA 1, PH-DATE 2, JX-QLD 1, PG-HEADER 1, DUP-SENT 3.
6. D6 (report PDF rendering) awaits the source of the reviewed draft report.

## Portal (local, A-21)
```
pip install -r requirements.txt
export TMPCHECK_ENV=local
python -m src.portal.devseed --org "Way to Go Traffic Management" --user "Your Name" --email you@example.com --role customer_reviewer   # prompts for a password (10+ chars)
uvicorn src.portal.app:app --port 8000
python -m pytest tests/portal
# Test states (local DB only): python -m src.portal.devtools sub active | credits 10 | use-credit | check REF-001 draft_review --findings Major=2 | reset
```
Stage plan: `docs/DASHBOARD_IMPLEMENTATION_PLAN.md` §5. S1 done; next S2 (accounts). S3 needs P-14, P-15.
2. Customer files are **not** in Git. Owner re-uploads `SU026_redacted.pdf` and `SU026_Shoalwater_TMP_Proofread_Rev0.pdf` to the chat; copy to `customer-docs/wtgtm-2026-11-20/`. Recreate `REF-01.expected.json` and `out/adj_det.json` (also git-ignored) — row list in BENCH-02 session; if lost, re-transcribe from the report.
3. Fetch public template: see `test-library/public/README.md`. `template_diff` takes the **.docx**, not the PDF.
4. Run: `python3 -m src.tmpcheck.llm_checks customer-docs/wtgtm-2026-11-20/SU026_redacted.pdf customer-docs/wtgtm-2026-11-20/out/llm.json`
5. Score with `src.tmpcheck.score` (commands in `docs/reviews/BENCH-02`); adjudicate unmatched findings; record in TEST_REGISTER and BENCH-02.
6. Record actual cost per check in COMMERCIAL_MODEL.md.

## Outstanding
See DECISIONS.md (pending), RISKS.md, PROJECT_PLAN.md.

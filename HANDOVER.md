# HANDOVER — TMP Check (current state)

_Last updated: 2026-11-25 by AI-PM_

## Current state
| Gate | Status |
|---|---|
| G1 Initiation | User accepted (A-13) |
| G2 Customer requirements | In progress — REF-01 report + source TMP received; analysis 01 done |
| G3 Compliance framework | User accepted, conditional (A-17) — Tara accreditation details + review pack due 2026-11-27 |
| G4 Working prototype | In progress — deterministic checks done; LLM passes coded, awaiting API key |

## Repository
Private: https://github.com/abovethetableglobal-au/TMP-Proof-Reader (branch `main`). Cloud environment: **TMP-Proof-Reader** (personal).

## Code
| Module | Purpose |
|---|---|
| `src/tmpcheck/template_diff.py` | Missing Main Roads template headings (rule WA-COP-4.2.1-001) |
| `src/tmpcheck/det_checks.py` | Placeholders, jurisdiction wording, missing headers, repeated sentences (no LLM) |
| `src/tmpcheck/llm_checks.py` | Claude API passes A–D, structured findings, evidence validation, cost logging |
| `src/spike/completeness_spike.py` | Spike S-01 (annotation prototype) |
| `compliance/rules/*.yaml` | 22 approved WA rules |

## Next session — exact steps
Branch `g4-postprocess-fixes` holds review-defect fixes D1–D5 (`src/tmpcheck/postprocess.py`); check it out.
Owner approved up to US$5 for passes A–D on SU_025 (A-22). SU_025 is historical (A-21).
1. Confirm key: `python3 -c "import os;print(bool(os.environ.get('ANTHROPIC_API_KEY')))"` → `True`.
2. Owner re-uploads `SU_025_Kanimbla_Road_Nedlands.pdf`; copy to `customer-docs/wtgtm-2026-11-20/` (git-ignored).
3. Run: `python3 -m src.tmpcheck.llm_checks customer-docs/wtgtm-2026-11-20/SU_025_Kanimbla_Road_Nedlands.pdf customer-docs/wtgtm-2026-11-20/out/llm.json` — stop if a pass exceeds US$2.
4. Log cost per pass in COMMERCIAL_MODEL.md and PROJECT_LOG.md.
5. Deterministic baseline on SU_025 (2026-11-25): PH-TBA 4, PH-ANGLE 3, JX-MRWA 1, PH-DATE 2, JX-QLD 1, PG-HEADER 1, DUP-SENT 3.
6. D6 (report PDF rendering) awaits the source of the reviewed draft report.

## Outstanding
See DECISIONS.md (pending), RISKS.md, PROJECT_PLAN.md.

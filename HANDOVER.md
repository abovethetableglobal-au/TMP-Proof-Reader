# HANDOVER — TMP Check (current state)

_Last updated: 2026-11-20 by AI-PM_

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
1. Confirm key: `python3 -c "import os;print(bool(os.environ.get('ANTHROPIC_API_KEY')))"` → `True`.
2. Customer files are **not** in Git. Owner re-uploads `SU026_redacted.pdf` and `SU026_Shoalwater_TMP_Proofread_Rev0.pdf` to the chat; copy to `customer-docs/wtgtm-2026-11-20/`.
3. Fetch public template: see `test-library/public/README.md`.
4. Run: `python3 -m src.tmpcheck.llm_checks customer-docs/wtgtm-2026-11-20/SU026_redacted.pdf customer-docs/wtgtm-2026-11-20/out/llm.json`
5. Score LLM + deterministic findings against REF-01 (~105 items); record in TEST_REGISTER and `docs/reviews/BENCH-02`.
6. Record actual cost per check in COMMERCIAL_MODEL.md.

## Outstanding
See DECISIONS.md (pending), RISKS.md, PROJECT_PLAN.md.

# HANDOVER — TMP Check (current state)

_Last updated: 2026-11-25 by AI-PM_

## Current state
| Gate | Status |
|---|---|
| G1 Initiation | User accepted (A-13) |
| G2 Customer requirements | In progress — REF-01 report + source TMP received; analysis 01 done |
| G3 Compliance framework | User accepted, conditional (A-17) — Tara accreditation details + review pack due 2026-11-27 |
| G4 Working prototype | In progress — LLM passes run on REF-01-SRC: recall 86% (95/110), US$2.62/check (BENCH-03); precision not yet adjudicated |

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
1. Confirm key: `python3 -c "import os;print(bool(os.environ.get('TMPCHECK_ANTHROPIC_API_KEY')))"` → `True`.
2. Customer files are not in Git: SU026 pair → `customer-docs/wtgtm-2026-11-20/`; check 14/15 outputs → `customer-docs/su025-check14/` (re-upload if needed).
3. Owner/WTGTM: adjudicate the ~55 additional BENCH-03 findings and the disputed Note 2 cone spacing item → record precision in TEST_REGISTER L-01.
4. Fix DEF-D03-1 (style variants downgraded), DEF-D03-3 (punctuation rules); re-run once to measure variance between runs.
5. Portal fixes are on branch `claude/portal-postprocess-fixes` (portal + `g4-postprocess-fixes` merged); see PROJECT_LOG 2026-11-25.

## Outstanding
See DECISIONS.md (pending), RISKS.md, PROJECT_PLAN.md.

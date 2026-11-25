# HANDOVER — TMP Check (current state)

_Last updated: 2026-11-25 by AI-PM. Short-form restart notes: `handovers/attg.md`_

## Authoritative record
`main` is the single authoritative line (Owner approval 2026-11-25). On 2026-11-25 all working branches were merged into `main`, and colliding record IDs were renumbered (see the ID reconciliation table in DECISIONS.md). Future sessions branch from `main` and merge back. Do not start work from an old `claude/*` branch.

## Current state
| Gate | Status |
|---|---|
| G1 Initiation | User accepted (A-13) |
| G2 Customer requirements | In progress — REF-01 + SU026 source analysed; SU 025 received; Tara feedback FB-01 |
| G3 Compliance framework | User accepted, conditional (A-17) |
| G4 Working prototype | In progress — portal produces a report and an annotated PDF; engine 92% recall on SU026 two-run (BENCH-05); untuned single run 86% (BENCH-06); awaiting Owner review of the outputs. Not passed |
| G5–G8 | Not started (pricing, legal and launch-plan drafts exist: A-31 to A-40) |

## Code
| Module | Purpose |
|---|---|
| `src/portal/` | Local customer portal (A-21): sign-in, roles, upload → checks → reviewer workflow → final outputs |
| `src/tmpcheck/det_checks.py` | Rule checks: placeholders, interstate (Moderate, A-30), MRWA wording (Query), word-form, headers, repeated sentences; an action for every rule |
| `src/tmpcheck/llm_checks.py` | Claude passes A–D (+ draft pass E risk review, not enabled in the portal); key `ANTHROPIC_API_KEY` or `TMPCHECK_ANTHROPIC_API_KEY` (cloud sessions) |
| `src/tmpcheck/postprocess.py` | Shared word-level evidence locator, validation (unlocated → Query, VISUAL-only Critical → Query), merging |
| `src/tmpcheck/consolidate.py` | AI grouping of duplicate issues across passes and runs |
| `src/tmpcheck/outputs.py` | Report PDF and annotated TMP |
| `src/tmpcheck/score.py` | Scores findings against a reference JSON |
| `compliance/rules/*.yaml`, `compliance/risk_catalogue.yaml` | 22 WA rules plus 2 under review; expected-risk prompts for pass E |

Tests: `python -m pytest -q` → 53 pass.

## Portal (local)
```
pip install -r requirements.txt
export TMPCHECK_ENV=local
python -m src.portal.devseed --org "Way to Go Traffic Management" --user "<name>" --email <email> --role customer_reviewer
python -m uvicorn src.portal.app:app --port 8000   # Windows: plain "uvicorn" may not be on PATH
```

## Owner decisions needed
1. **Prices in the portal:** done — A-44 ($349 base).
2. **Pass E (risk review):** a draft that has not been benchmarked. Its uncited Moderate/Major findings conflict with the scope text for category E ("potential issue only where a rule is cited"). Decide on its category before it is enabled.
3. **FB-01 (Tara, SU 025):** Criticals F-001 and F-002 may not apply (works are on the verge, R-28). The AI-PM text check found both supported by the TMP's own conflicting statements. Reviewer to rule.

## Next session — exact steps
1. Key: `python3 -c "import os;print(bool(os.environ.get('TMPCHECK_ANTHROPIC_API_KEY') or os.environ.get('ANTHROPIC_API_KEY')))"` → `True`.
2. Customer files are not in Git (re-upload when needed): the SU026 pair → `customer-docs/wtgtm-2026-11-20/`; SU 025 and the check 14/15 outputs → `customer-docs/su025-check14/`.
3. Owner re-runs check 14 (SU 025) in the portal on the PC with `main` to confirm DEF-C14-1 to 6 (TEST_REGISTER).
4. Owner/WTGTM adjudicate the additional BENCH-06 findings and the TGS Note 2 cone-spacing dispute → record precision.
5. Fix DEF-L06-1 (style-variant findings downgraded) and DEF-L06-3 (punctuation rules).

## Outstanding
See DECISIONS.md (pending), RISKS.md, PROJECT_PLAN.md, DELIVERABLES.md.

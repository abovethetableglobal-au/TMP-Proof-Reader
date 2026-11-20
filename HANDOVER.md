# HANDOVER — TMP Check (current state)

_Last updated: 2026-11-20 by AI-PM_

## Current state
- Phase: Gate 1 (Initiation) — records complete, awaiting Owner sign-off.
- No code written yet (by design — awaiting real WTGTM documents).
- Compliance: source register started; 0 rules.

## Architecture
See `docs/ARCHITECTURE.md` (proposed, not approved). Stage 1 = local Python pipeline; portal/payments deferred.

## Repository
Private: https://github.com/abovethetableglobal-au/TMP-Proof-Reader (branch `main`).

## Repository layout
| Path | Purpose |
|---|---|
| `*.md` (root) | Project management records (handover §15) |
| `PROJECT_HANDOVER.md` | Original Owner brief v1.0 (authoritative) |
| `docs/` | Evidence request, test methodology, architecture |
| `compliance/sources/` | Source notes (no copyrighted full text) |
| `compliance/rules/` | YAML rules + `_schema.yaml` |
| `test-library/` | Anonymised test docs + reference findings |
| `customer-docs/` | Live customer docs — **git-ignored, never commit** |

## Setup
Nothing to install yet. Prototype prerequisites (Stage 1): Python 3.11, LibreOffice, Tesseract, ocrmypdf, ClamAV, Anthropic API key (via environment secret — never committed).

## Outstanding issues
See DECISIONS.md "Pending" and RISKS.md. Blocking: P-03 (reviewer), WTGTM evidence.

## Next steps
See PROJECT_PLAN.md "Immediate priorities".

# TMP Draft Builder — outline v0.1 (deferred, A-42)

Status: Not started. Trigger: 6 paying customers. Not approved scope.

## Flow
1. Intake: structured form plus the tender PDF (location, road class, speed, AADT, works, staging, hours, detours, client clauses).
2. Gap check: missing inputs become visible [TBC] placeholders. Nothing is invented.
3. Assemble: MRWA TMP template structure. TGS suggested only from an approved library, with the source cited.
4. Draft text: AI writes narrative only from the inputs and cited sources. The risk register is seeded from `compliance/risk_catalogue.yaml`; ratings are left blank for the RTM.
5. Layout: Word (MRWA format) is the master. Canva is used for the cover, site graphics and summary pages.
6. Self-check with the TMP Check engine.
7. The accredited RTM completes and signs. The tool never marks a draft final.

## Preconditions
- Change request under Master Prompt §20.1; conflicts with CLAUDE.md §2 (no design) to be resolved.
- Liability/legal review; Terms of Service update.
- Licence check for MRWA images and examples (WA Government copyright).
- G6 data handling for client data in Claude and Canva.
- Pricing (not covered by A-31 to A-33).

## Phases
1. Scope and legal. 2. Intake + gap check + one work type. 3. TGS library, Word output, Canva cover. 4. Self-check + pilot on a historical WTGTM job (A-18).

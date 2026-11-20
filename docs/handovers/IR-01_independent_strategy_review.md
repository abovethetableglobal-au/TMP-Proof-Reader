# IR-01 — Independent Strategy Review (AI handover, Master Prompt §4.5)

**Delegated to:** ChatGPT or Gemini (human-mediated — Owner copies this brief and the listed files, then pastes the response back to Claude Code)
**Issued:** 2026-11-20 · **Status:** Awaiting approval (Owner to transfer)

## Objective
Provide an independent critical review of the TMP Check project strategy, plan and risk register, identifying weaknesses, omissions and better alternatives.

## Context
TMP Check is an AI-assisted quality-checking service for Traffic Management Plans (TMPs) used for works on roads in Western Australia. Founding customer is a WA traffic management company that currently pays ~$405 AUD per outsourced proofread. Pricing: $49.95/month subscription + $149 per check credit (10-pack $1,341). Every pilot report is reviewed by a human before release. The product is document QA only — not approval or certification. Compliance baseline: Main Roads WA Traffic Management for Works on Roads Code of Practice (March 2026), which adopts AGTTM Ed 1.1 (Parts 1–7, 9, 10), Ed 2.0 (Part 8) and AS 1742.3-2019.

## Inputs attached (Owner to paste or upload)
1. `PROJECT_BRIEF.md`
2. `PROJECT_PLAN.md`
3. `RISKS.md`
4. `COMMERCIAL_MODEL.md`
5. `docs/ARCHITECTURE.md`
6. `docs/reviews/TPR-01_project_strategy.md`

Do **not** attach any customer documents.

## Constraints
- Do not invent regulatory requirements or statistics; mark any claim you cannot source as an assumption.
- Do not rewrite the documents; critique them.
- Approved commercial decisions (prices, credit rules) may be challenged but must be identified as Owner decisions.

## Expected output format
Markdown with these sections:
1. Top 5 weaknesses (ranked, each with evidence/reasoning and a concrete fix)
2. Missing risks (table: risk, impact, likelihood, mitigation)
3. Disagreements with TPR-01 (if any), with reasoning
4. Commercial model observations
5. One-paragraph overall verdict

## Acceptance criteria
- Each point is specific to this project (not generic SaaS advice).
- Each recommendation is actionable.
- Facts are distinguished from assumptions.
- ≤ 1,500 words.

## Return instructions
Owner pastes the full response into the Claude Code session, stating which platform and model produced it. Claude Code will assess it, record the outcome in `AI_RESOURCES.md`, and reconcile per Master Prompt §22.

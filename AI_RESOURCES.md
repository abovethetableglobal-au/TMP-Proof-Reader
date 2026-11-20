# AI_RESOURCES — Organisation, Capability Register & Delegation Log

Governed by Master Prompt v1.4 §4. No work is recorded as performed by another AI unless an actual integration or human-mediated handover occurred. All delegated output is reviewed by the AI-PM before use.

## 1. Organisation (Master Prompt §4.1)
| Department | Members | Responsibilities on TMP Check |
|---|---|---|
| Executive leadership | Claude Code (AI-PM) | Direction, planning, records, integration, accountability |
| Strategic & advisory | ChatGPT / Gemini (human-mediated) | Independent strategy/rule-draft review (IR-xx) |
| Technical & production | Claude Code + execution container; Anthropic Claude API (proposed) | Prototype pipeline, checking engine, outputs |
| Research | Claude Code via Firecrawl (integrated) | Public regulatory sources |
| Quality assurance | Tara — WTGTM accredited reviewer (human, A-15) | Rule review (G3), blind reference findings (G5), review/approval of every report (self-approve) |
| Customer | WTGTM | Evidence, feedback, pilot |

## 2. Capability & resource register (Master Prompt §4.3) — verified 2026-11-20
| Resource | Access / integration | Permissions | Limitations | Cost |
|---|---|---|---|---|
| Claude Code (this session) | Cloud container | Read/write files, run code, web research | Container ephemeral — persist via GitHub | Owner's Claude plan |
| GitHub `abovethetableglobal-au/TMP-Proof-Reader` | Attached to session | Push to repo | `gh` CLI token invalid in container (git push works) | Free (private repo) |
| Firecrawl search/scrape | Integrated MCP tool | Public web only | AI "query" extraction must be verified manually | Owner's Firecrawl credits — ~180 used on 2026-11-20 |
| Google Drive | Connector available | Not yet used | Not approved for customer docs | — |
| Gmail / Google Calendar | Connector available | Not used | Sending to WTGTM requires Owner approval | — |
| Anthropic Claude API | **Not configured** | — | Needs API key + approval (P-04) | Pay per use |
| ChatGPT / Gemini | **No integration** | Human-mediated only | Owner must transfer briefs/results | Owner's plans |
| Tara (WTGTM) | Appointed A-15 | Customer-side reviewer | Single reviewer (R-18); not independent of customer (R-17) | Borne by WTGTM (S-05) |

## 3. Delegation log
| Task ID | Date | Resource | Brief | Acceptance criteria | Outcome | Review |
|---|---|---|---|---|---|---|
| AT-01 | 2026-11-20 | Firecrawl | Identify current WA Code edition and adopted AGTTM/AS editions | Primary source (mainroads.wa.gov.au) | WA Code Mar 2026; AGTTM Ed 1.1 (Pts 1–7,9,10), Ed 2.0 (Pt 8); AS 1742.3–2019 | Edition accepted (primary source). Section content flagged AI-X — AI extraction of a 158-pp PDF; manual verification required |
| AT-02 | 2026-11-20 | Firecrawl | Summary of March 2026 amendments | Cross-check with Code revision record | Secondary source (AusQ Training) | Accepted as lead list only; not authoritative |
| IR-01 | 2026-11-20 | ChatGPT or Gemini (human-mediated) | Independent strategy review — `docs/handovers/IR-01_independent_strategy_review.md` | Per brief | **Not yet transferred** | — |

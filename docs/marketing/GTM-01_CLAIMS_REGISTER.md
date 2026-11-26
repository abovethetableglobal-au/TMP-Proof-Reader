# GTM-01 Claims and Substantiation Register · v0.1 (2026-11-26)
Status: Ready for user review. Every customer-facing claim must appear here, with its evidence, before it is used. A claim marked Hold or Banned must not appear in any published asset.

| ID | Claim (exact wording) | Evidence | Class (§18.2) | Status | Condition to use |
|---|---|---|---|---|---|
| C-01 | "Every finding cites the source, edition and clause." | CLAUDE.md §2; uncited items are raised as Query | Verified fact (design rule) | Usable | Re-verify on the G5 sample |
| C-02 | "Your accredited reviewer accepts, edits or rejects every finding before the final report is issued." | A-15; portal draft→disposition→final flow | Verified fact | Usable | — |
| C-03 | "About 8 minutes processing for an 81-page TMP in testing." | Checks 14/15, BC 016: 7 min 40 s, 7 min 51 s | Verified fact (2 runs, 1 document) | Usable with qualifier | Keep "in testing"; must not imply total turnaround time |
| C-04 | "Reviewer time: about 1 hour, compared with 5+ hours of manual checking." | BENCH-05 estimate 51–76 min; Tara 5+ h (FB-01) | Estimate | Hold | Timed reviews in the G7 pilot (median ≤ 2 h target) |
| C-05 | "X% recall across N benchmark TMPs." | BENCH-05: 92% on 1 TMP (SU026) | Source-supported conclusion (n=1) | Hold | G5 multi-document benchmark |
| C-06 | "N WA Code of Practice rule checks reviewed by an AWTM-accredited reviewer." | A-17, conditional; prototype use only | Verified fact (conditional) | Hold | A-17 condition closed and rules approved for live use (G6) |
| C-07 | "Every Major finding is confirmed by two AI runs or a rule check." | Not supported: check 15 had 51 one-run findings | — | Banned | P-24 option B built and tested |
| C-08 | "Findings labelled Both runs / One run / Rule check." | Consistency label, portal 2026-11-25 | Verified fact | Usable | — |
| C-09 | "Your original TMP is never modified; annotations go on a separate copy." | CLAUDE.md §2 | Verified fact (design rule) | Usable | — |
| C-10 | "Australian-hosted, encrypted document storage." | P-20 pending | — | Hold | G6 / P-20 approved |
| C-11 | Prices: $49.95/month; $349; $1,657.75 (5-pack); $3,141 (10-pack); credits valid 12 months; not registered for GST | config/portal.yaml; A-31–A-33 | Verified fact | Usable | Re-pull from config at publish time |
| C-12 | "Checks against AS 1742.3." | Deferred to G8 (A-35, R-26) | — | Hold | AS rules added and benchmark re-run |
| C-13 | Tagline "Check • Cite • Confident" | A-51 | Verified (Owner decision) | Usable | — |

**Banned words (all assets):** approved, compliant, compliance-checked, certified, safe, guaranteed, 100%, error-free, "catches everything".
**Mandatory safety line:** "TMP Check is document QA. It does not approve, certify or declare a TMP safe. Your accredited reviewer makes the final call."

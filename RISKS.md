# RISKS — TMP Check

Scale: L/M/H. Score = Impact × Likelihood.

| ID | Risk | Impact | Likelihood | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | AI misses a safety-critical issue; customer relies on report | H | M | Human review gate; explicit limitations; "no issue identified in this check" wording; defect monitoring post-launch | AI-PM / Reviewer | Open |
| R-02 | Hallucinated or mis-cited compliance findings | H | H (unmitigated) | Findings must quote extracted evidence + rule ID; automated evidence validation; uncited → Query | AI-PM | Open |
| R-03 | Human review cost erodes margin — **mostly transferred to customer by A-15**; residual: long reviews erode WTGTM's saving | M | M | Measure review time from first prototype run; design reviewer UI for speed; target ≤45 min/check | AI-PM | Open |
| R-04 | Wrong standard edition applied (e.g. AGTTM 1.2 used where WA adopts 1.1) | H | M | Version-locked compliance library; per-rule edition field; jurisdiction check | AI-PM | Open |
| R-05 | Customer document confidentiality breach | H | L | Anonymised dev data; git-ignored customer folder; approved AI provider; AU-hosted storage; audit log | AI-PM / Owner | Open |
| R-06 | WTGTM evidence delayed (holiday period) | M | H | Send request now; start on public MRWA templates | Owner | Open |
| R-07 | No qualified reviewer appointed → Gate 3/5 blocked | H | M | Tara appointed (A-15) | Owner | Closed 2026-11-20 |
| R-08 | Copyright breach reproducing Standards text | M | M | Paraphrase requirements; cite clause only; licensed copies held | AI-PM | Open |
| R-09 | Liability/claims from reliance on reports | H | L | Terms of service + disclaimer reviewed by a lawyer before pilot; professional indemnity insurance enquiry | Owner | Open |
| R-10 | GST registration obligation arises as turnover grows | M | M | Configurable GST; Owner to obtain accountant advice | Owner | Open |
| R-11 | Drawing/TGS interpretation unreliable (images, CAD PDFs) | M | H | Start with text-layer extraction; flag drawing checks as Query where uncertain; measure accuracy separately | AI-PM | Open |
| R-12 | Low/unknown WTGTM volume → weak economics | M | M | Obtain monthly volume in evidence request | Owner | Open |
| R-13 | Project records lost (ephemeral container, no remote) | M | H | Pushed to private repo (A-11) | Owner | Closed 2026-11-20 |
| R-14 | Over-building before validation | M | M | Gate discipline; payments deferred to post-G5 | AI-PM | Open |
| R-15 | Delivery depends on Owner manually performing checks (non-scalable) | M | M | Reviewer role separable from Owner; SOPs | AI-PM | Open |
| R-16 | Automation bias — customer reviewer over-relies on draft findings and misses issues TMP Check did not raise | H | M | Report states scope & limitations; reviewer attests per check; track reviewer edits/rejections; never imply "no issues" | AI-PM | Open |
| R-17 | Rule set reviewed only by the founding customer's staff — not independent for other customers | M | M | Before G8/expansion: independent accredited review of rule library | Owner | Open |
| R-18 | Single reviewer (Tara) — availability bottleneck for G3, G5 and pilot turnaround | M | M | Agree time commitment; nominate backup accredited WTGTM reviewer | Owner | Open |
| R-19 | Ground truth not blind — reviewer sees TMP Check output before setting reference findings | H | M | Tara sets reference findings **before** seeing any TMP Check output (TEST_METHODOLOGY §1) | AI-PM | Open |
| R-20 | Reviewer accreditation assumed, not verified (S-07); if RTM not held, complex TMPs need another endorser | M | L | Sight accreditation records (level, number, expiry) before G3; record in AI_RESOURCES | AI-PM | Open |
| R-21 | Credential exposure — an Anthropic token was pasted into chat on 2026-11-20 | M | L | Owner revoked it the same day; keys only via environment variable; AI-PM never stores or echoes keys | Owner | Closed 2026-11-20 |
| R-22 | Customer documents used on verbal permission only — no written record; contradicts request v0.2 wording | M | M | Owner decision A-18; files held only in git-ignored `customer-docs/`; not shared or used for training; seek one-line written confirmation when convenient | Owner | Open |

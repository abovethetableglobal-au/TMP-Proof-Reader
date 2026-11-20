# RISKS — TMP Check

Scale: L/M/H. Score = Impact × Likelihood.

| ID | Risk | Impact | Likelihood | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| R-01 | AI misses a safety-critical issue; customer relies on report | H | M | Human review gate; explicit limitations; "no issue identified in this check" wording; defect monitoring post-launch | AI-PM / Reviewer | Open |
| R-02 | Hallucinated or mis-cited compliance findings | H | H (unmitigated) | Findings must quote extracted evidence + rule ID; automated evidence validation; uncited → Query | AI-PM | Open |
| R-03 | **Human review cost erodes margin** — at $75/hr, >2 hrs review exceeds the $149 credit | H | H | Measure review time from first prototype run; design reviewer UI for speed; target ≤45 min/check | AI-PM | Open |
| R-04 | Wrong standard edition applied (e.g. AGTTM 1.2 used where WA adopts 1.1) | H | M | Version-locked compliance library; per-rule edition field; jurisdiction check | AI-PM | Open |
| R-05 | Customer document confidentiality breach | H | L | Anonymised dev data; git-ignored customer folder; approved AI provider; AU-hosted storage; audit log | AI-PM / Owner | Open |
| R-06 | WTGTM evidence delayed (holiday period) | M | H | Send request now; start on public MRWA templates | Owner | Open |
| R-07 | No qualified reviewer appointed → Gate 3/5 blocked | H | M | Decide P-03 early | Owner | Open |
| R-08 | Copyright breach reproducing Standards text | M | M | Paraphrase requirements; cite clause only; licensed copies held | AI-PM | Open |
| R-09 | Liability/claims from reliance on reports | H | L | Terms of service + disclaimer reviewed by a lawyer before pilot; professional indemnity insurance enquiry | Owner | Open |
| R-10 | GST registration obligation arises as turnover grows | M | M | Configurable GST; Owner to obtain accountant advice | Owner | Open |
| R-11 | Drawing/TGS interpretation unreliable (images, CAD PDFs) | M | H | Start with text-layer extraction; flag drawing checks as Query where uncertain; measure accuracy separately | AI-PM | Open |
| R-12 | Low/unknown WTGTM volume → weak economics | M | M | Obtain monthly volume in evidence request | Owner | Open |
| R-13 | Project records lost (ephemeral container, no remote) | M | H | P-02: push to private repo | Owner | Open |
| R-14 | Over-building before validation | M | M | Gate discipline; payments deferred to post-G5 | AI-PM | Open |
| R-15 | Delivery depends on Owner manually performing checks (non-scalable) | M | M | Reviewer role separable from Owner; SOPs | AI-PM | Open |

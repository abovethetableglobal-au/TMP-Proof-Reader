# COMPLIANCE_REGISTER — TMP Check (WA)

Status legend: **V** verified against primary source by AI-PM · **AI-X** extracted by an AI tool, pending manual verification · **PR** professionally reviewed · **—** not started.

## 1. Source register
| Src ID | Source | Edition / date | Authority | Official URL | Status | Verified |
|---|---|---|---|---|---|---|
| SRC-WA-COP | Traffic Management for Works on Roads Code of Practice | March 2026 (158 pp) | Main Roads WA | https://www.mainroads.wa.gov.au/globalassets/technical-commercial/working-on-roads/traffic-management/traffic-management-for-works-on-roads-code-of-practice.pdf | V for §3.5, §4.2.1–4.2.3 (primary text read); other sections AI-X | 2026-11-20 |
| SRC-AGTTM-1-7,9,10 | Austroads Guide to Temporary Traffic Management Parts 1–7, 9, 10 | **Edition 1.1, 2021** (as adopted by WA Code) | Austroads (adopted by MRWA) | https://austroads.gov.au/network-operations/temporary-traffic-management/guide | AI-X | 2026-11-20 |
| SRC-AGTTM-8 | AGTTM Part 8 | **Edition 2.0, 2025** (as adopted by WA Code) | Austroads (adopted by MRWA) | as above | AI-X | 2026-11-20 |
| SRC-AGTTM02-11 | AGTTM Part 2 Ed 1.1 (AGTTM02-21), App B Table B1 risk checklist (pp 49–52) | Edition 1.1, Sept 2021 (WA-adopted) | Austroads | https://austroads.gov.au/publications/temporary-traffic-management/agttm02-21 | AI-PM read primary text (Owner copy); identical to Ed 1.2 Table B.1 | 2026-11-24 |
| SRC-AGTTM02-12 | AGTTM Part 2 Ed 1.2 (AGTTM02-26), App B Table B.1 risk checklist | Edition 1.2, May 2026 (**not WA-adopted**, see VC-01) | Austroads | https://austroads.gov.au/publications/temporary-traffic-management/agttm02 | AI-PM read primary text (Owner copy) | 2026-11-24 |
| SRC-AS1742.3 | AS 1742.3:2019 Manual of uniform traffic control devices — Part 3: Traffic control for works on roads | 2019 | Standards Australia (adopted by MRWA) | Licensed purchase required (P-06) | — | — |
| SRC-WA-TMP-TPL | MRWA TMP template; Basic TMP template | Current on MRWA site | Main Roads WA | https://www.mainroads.wa.gov.au/technical-commercial/working-on-roads/ | V (exists) | 2026-11-20 |
| SRC-WA-GEN-CHK | Checklist to Determine the Need for Generic or Site Specific TMP | Current on MRWA site | Main Roads WA | as above | V (exists) | 2026-11-20 |
| SRC-WA-TGS-CHK | Example Onsite TGS Selection Checklist | Current on MRWA site | Main Roads WA | as above | V (exists) | 2026-11-20 |
| SRC-WA-SPEC202 | MRWA Specification 202 — Traffic Management | Check edition | Main Roads WA | https://www.mainroads.wa.gov.au/globalassets/technical-commercial/technical-library/specifications/200-series-management-requirements/specification-202-traffic-management-pdf.pdf | — | — |
| SRC-WA-TMA | Requirements for the use of TMAs in WA — Code of Practice | Check edition | Main Roads WA | https://www.mainroads.wa.gov.au/globalassets/technical-commercial/working-on-roads/traffic-management/requirements-for-the-use-of-TMAs-WA.pdf | — | — |
| SRC-LG-* | Local government requirements (e.g. City of Swan Traffic Management Guidelines 2026-27) | Per LGA | Local governments | https://www.swan.wa.gov.au/awcontent/Web/Documents/Planning-Building/Traffic-Management-Guidelines-2026-27.pdf | — | — |
| SRC-WTGTM-* | WTGTM templates, procedures, customer requirements | TBC | WTGTM | Customer-supplied | — | — |

## 2. Version-control findings
- **VC-01 (important):** The WA Code (March 2026) adopts AGTTM **Ed 1.1 (2021)** for Parts 1–7, 9, 10 and **Ed 2.0 (2025)** for Part 8. Austroads has since published AGTTM Ed 1.2. WA has **not** adopted Ed 1.2 per this Code. Rules must cite the WA-adopted edition. _Source: SRC-WA-COP, front matter — AI-X, verify manually._
- **VC-02:** The Code states that where it conflicts with AGTTM/AS 1742.3, **the Code takes precedence**. Rule precedence: Project-specific approval/permit > WA Code > AGTTM (adopted ed.) > AS 1742.3:2019 > LGA guidance > WTGTM internal. _(Precedence of project/LGA requirements to be confirmed by reviewer.)_
- **VC-04:** Code §4.2.1 **requires** a Main Roads TMP template to be used with all section headings retained. This supports the template-diff method for category C (Spike S-01 GAP-S01-1). Current template is the April 2026 edition (PUB-01).
- **VC-03:** March 2026 amendments of likely relevance to TMP checking (secondary source: AusQ Training summary; verify against Code revision record): §2.1 consultation before submission; §4.2.1 TMP preparation before site visit; §4.2.2 Generic TMP expectations; §4.2.6 sign position tolerances; §4.6 signs blocking footpaths; new §6.1.13 worker symbolic signs; new §6.1.14 lane status / turning movement signs, extended speed zones, All Traffic Turn sign; §6.8.1 Prepare to Stop sign position; §6.8.8 pilot vehicles; §8.2 PTCD training.

## 3. WA Code sections mapped to check categories (AI-X)
| Code § | Topic | Check category |
|---|---|---|
| 2, 2.1, 2.2 | Approval to work in road reserve (MRWA vs LGA roads) | E Compliance |
| 3.5 | Authorising TMPs | E Compliance / C Completeness |
| 4.2.1 | TMP — general content | C Completeness / E |
| 4.2.2 | Generic TMPs; TGS selection process | E / D Technical |
| 4.2.3 | TMPs involving complex traffic arrangements | E |
| 4.2.4 | Temporary road safety barrier detail | D / E |
| 4.2.5 | TM implementation & removal | C |
| 4.2.6 | Adjustment & modification of TMPs | E |
| 4.6 | Vulnerable road users — primary path closures (metro) | D / E |
| 5.2 | TM operation & records | C |
| 8.1–8.7 | Accreditation (TC, BWTM, WTM, AWTM, RTM, TMA operator) | E |

## 4. Rules
Schema: `compliance/rules/_schema.yaml`. Rule files: `compliance/rules/*.yaml`.
No rules are approved for live use. Count: **22 verified by AI-PM against primary text** / **22 reviewed by Tara (accepted, no amendments)** / **22 approved for prototype use** (A-17); live use from G6.

| Clause | Rules | Notes |
|---|---|---|
| §3.5 | WA-COP-3.5-001 | Authorising road authority |
| §4.2.1 | 001–010 | Template use, AWTM preparer, signatures, site visit + photo, contingency, TGS signing/labelling, 12-month review, watermarks |
| §4.2.2 | 001–002 | Generic TMP minimum content, TGS selection procedure |
| §4.2.3 | 001–005 | Complex-arrangement triggers → RTM endorsement; RTM ≠ preparer; no residual VH; risk assessment; WTM/AWTM on site (Main Roads roads) |
| §8 | 8.3-001/002, 8.7-001, 8.9-001 | BWTM on site; supervised sign placement limits; TMA operator accreditation; accreditation currency (Query) |

Page references use the Code's printed page numbers (printed page = PDF page − 1).

## 5. Review history
| Date | Reviewer | Scope | Outcome |
|---|---|---|---|
| 2026-11-20 | AI-PM | Source identification; WA Code edition & adopted references | Edition verified; content AI-extracted, manual verification pending |
| 2026-11-20 | AI-PM | §3.5, §4.2.1–4.2.3 primary text | 17 rules drafted & verified; awaiting Tara review |
| 2026-11-20 | AI-PM | §8 primary text | 5 rules added (22 total); core set complete for Tara review |
| 2026-11-20 | Tara (WTGTM), relayed by Owner | All 22 core rules | Accepted as written; no amendments, no additional rules proposed |

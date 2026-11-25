# COMMERCIAL_MODEL — TMP Check

All prices AUD. Approved by Owner 2026-11-20 (DECISIONS A-02–A-06).

## Price list — v2 structure (Owner approved 2026-11-25, A-31). Base price set 2026-11-25 (A-32)
Base per-check price `P` = **$349** (configuration `pricing.base_check`).

| SKU | Price | Included checks | Notes |
|---|---|---|---|
| Starter subscription | $49.95/month | 0 | Required to buy single checks ($349) and 5/10 packs; platform access |
| Single check | P | 1 | Starter subscribers only |
| 5-check value pack | 5 × P × 0.95 | 5 | 5% discount |
| 10-check value pack | 10 × P × 0.90 | 10 | 10% discount |
| Professional subscription | $1,495/month | 5/month ($299 each, −14%) | Extra checks $299; includes platform access |
| Business subscription | $3,995/month | 15/month ($266.33 each, −24%) | Extra checks $269; includes platform access |
| Enterprise | From $9,990/month (quoted) | Up to 40/month (≤$249.75 each) | Negotiated |

| Item | Price | Per check |
|---|---|---|
| Single check | $349.00 | $349.00 |
| 5-check pack (−5%) | $1,657.75 | $331.55 |
| 10-check pack (−10%) | $3,141.00 | $314.10 |

Ladder (per check): single $349 > 5-pack $331.55 > 10-pack $314.10 > Professional $299 > Business $266.33 > Enterprise ≤$249.75. Unused included checks do not roll over. Approved 2026-11-25 (A-33).

Superseded v1 (A-03–A-06): $149/check; 10-pack $1,341.

```yaml
pricing:
  base_check: 349.00        # A-32
  packs: {5: 0.05, 10: 0.10}
```

## Credit rules (approved)
1. Purchased upfront. 2. Added after successful payment. 3. 1 credit per completed check. 4. Failed upload/processing: no charge. 5. Correction of a TMP Check error: no charge. 6. Customer re-check after document changes: 1 credit. 7. Valid 12 months from purchase. 8. Balance and history visible to customer. 9. Subscription billed separately.

**Approved (A-39):** lapse = credits retained; cancel = unused credits forfeited. Consumption oldest-lot-first. **Pilot price (A-40):** $145/check for WTGTM during G7.

## Ledger design (to implement post-G5)
Append-only `credit_ledger` rows: `id, customer_id, lot_id, type{purchase, consume, reversal, expiry, adjustment}, qty(±), check_id?, payment_ref?, expires_at, created_at, created_by, reason`. Balance = Σqty of unexpired lots. Adjustments require admin + reason (audit).

## GST configuration
```yaml
tax:
  gst_registered: false      # Owner advice 2026-11-20
  gst_rate: 0.10             # applied only if gst_registered: true
  price_display: "excl"      # never label prices "GST-inclusive" while unregistered
```
Not tax advice. Owner to obtain accountant advice on registration threshold as turnover grows (R-10).

## Customer value benchmark
| Item | Amount |
|---|---|
| Historical outsourced check | $405 (9 hrs × $45) |
| 10 checks historical | $4,050 |
| TMP Check: 10-pack + 1 month sub | $1,390.95 |
| Difference | $2,659.05 (~65.7%) |

Assumes 10 comparable checks in one month and $405 is representative. $675 (9 hrs × WTGTM $75) is an opportunity-cost figure, **not** a cash saving. No savings guarantees.

## Cost & margin assumptions (to be measured — all PROVISIONAL)
| Cost driver per check | Assumption | Basis |
|---|---|---|
| AI processing | $2–$15 (measured US$2.62 for one A–D run on a 61-pp TMP; portal ×2 runs ≈ US$5–6, check 14 = US$6.10 for 64 pp) | BENCH-06 2026-11-25 (verified fact for SU026); range kept for larger TMPs |
| Human review (pilot) | $0 to TMP Check — performed by customer's accredited reviewer (A-15) | Cost borne by customer; reduces their net saving |
| Hosting/storage | < $1 | Small-scale cloud |
| Payment fees | ~1.75%–2.9% + fixed | Provider TBD |

**Our contribution per credit (estimate):** ≈ $149 − AI/infra (~$3–16) − payment fees ≈ **$128–143**.

**Customer net saving per check (estimate):** $405 − $149 − (reviewer hrs × $75). At 1 hr review ≈ $181; at 2 hrs ≈ $106. Reviewer time remains a key metric because it drives the customer's value.

**Measured 2026-11-20 (OWNER-FT-02):** AI processing US$3.33 for SU026 (61 pp, passes A–D) ≈ A$5. Within the $2–15 assumption.
**Measured 2026-11-20 (BENCH-05, A-27 two-run default):** US$4.86 (≈ A$7.40) per 61-page TMP.
## Revenue scenario — 2% of WA TMPs checked (ESTIMATE, 2026-11-24)
WA annual TMP volume is unverified (no public data; FB-01 triage), so three volume assumptions are used. Each subscriber is assumed to do 4 checks/month (48/yr); credits are assumed bought as 10-packs ($134.10). Contribution per credit ≈ $115–128 after AI ($3–16) and ~2.5% payment fees.

| WA TMPs/yr (assumption) | Checks/yr (2%) | Subscribers | Subscription $/yr | Credits $/yr | Total $/yr | ≈ $/month | Contribution $/yr |
|---|---|---|---|---|---|---|---|
| 10,000 | 200 | 4 | 2,398 | 26,820 | 29,218 | 2,435 | 25–28k |
| 20,000 | 400 | 8 | 4,795 | 53,640 | 58,435 | 4,870 | 51–56k |
| 40,000 | 800 | 17 | 10,190 | 107,280 | 117,470 | 9,789 | 102–112k |
Excludes Owner time, marketing, support, and reviewer cost (borne by customer). Above ~$75k turnover, GST registration review is triggered (R-10).

## WA market size — firm count (MKT-01, 2026-11-25)
| Source (Main Roads WA, retrieved 2026-11-25) | Count | Evidence |
|---|---|---|
| Registered TM Company list — Traffic Management Companies | 60 | Verified fact (AI-extracted count from PDF; 91–92 total entries) |
| — Contractors | 20 | Verified fact (as above) |
| — Local Government | 11 | Verified fact |
| — State Government | 1 | Verified fact |
| Accredited RTMs (list as of 19 Nov 2026) | 38 people / 30 employers | Verified fact; 6 at Main Roads |

Interpretation (Estimate): core addressable WA market ≈ 60 TM companies + ~10–20 TMP design consultancies not on the registration list (e.g. RTM employers) ≈ 70–90 organisations; contractors/LGs secondary. Customer forecast (Estimate, PROVISIONAL): Year 1 3–6; Year 2 8–15; WA ceiling 20–35 (25–40% share of core). Supersedes the unsourced 100–200 firm / 30–60 customer estimate given in chat. Overlap between lists not checked.

## Australian and international market (MKT-02, 2026-11-25)
- MKT-01 review: WA list types sum to 92 vs 91 total (extraction ±1). RTM list ≠ TMP writers; WA TMPs are written by AWTM-accredited people (count not published) — RTMs indicate complex-TMP capacity only.
- QLD TMR Register of Traffic Management Organisations (as at 2 Sep 2026): ~146 entries (Verified fact, AI-extracted, ±).
- Other states (Estimate): scaled at ~20–26 TM firms per million people (WA 60/3.0M; QLD 146/5.6M): NSW 170–220, VIC 140–180, SA 40–50, TAS/ACT/NT 25–35. Australia total ≈ 580–700 TM firms (+ design consultancies). RevenueBase lists 198 AU "traffic control companies" (database undercount).
- Each state needs its own rule pack (AGTTM national base + state supplements, e.g. QLD QGTTM, NSW TfNSW TCAWS, VIC code of practice).
- International (Hypothesis, unverified): NZ (NZGTTM), UK (Chapter 8 / Red Book), US (MUTCD Part 6) — different standards; competing software exists (e.g. TGS drawing tools). Defer until AU product proven.

## Demand-side sizing — TMPs per year (MKT-03, 2026-11-25)
No public count of TMPs/roadworks per year found (search 2026-11-25). Bottom-up Estimate: WA ≈ 60 TM firms × 10–25 site-specific TMPs/month + councils/utilities ≈ 10,000–20,000 site-specific TMPs/yr (generic TGS-only works excluded). Australia ≈ ×10 ≈ 100,000–200,000/yr.
| Market | TMPs/yr | Share checked | Checks/yr | Customers (48/yr) | Revenue/yr |
|---|---|---|---|---|---|
| WA | 10,000 | 2% / 5% / 10% | 200 / 500 / 1,000 | 4 / 10 / 21 | $65k / $163k / $327k |
| WA | 20,000 | 2% / 5% / 10% | 400 / 1,000 / 2,000 | 8 / 21 / 42 | $130k / $327k / $653k |
| AU | 150,000 | 2% / 5% | 3,000 / 7,500 | 63 / 156 | $0.98M / $2.45M |
Revenue = checks × $314.10 + subscribers × $599.40/yr. Cross-check: consistent with firm-count forecast (MKT-01/02). Validate with WTGTM monthly TMP volume and a council/Main Roads count.

## MKT-03 update — WTGTM volume (Owner, 2026-11-25)
WTGTM writes 8 site-specific TMPs/month (Owner-supplied fact). Replaces 10–25/firm Estimate with ~8–12 avg (Estimate; firm sizes vary). WA ≈ 60 × 8–12 × 12 + councils/utilities ≈ 6,000–10,000 TMPs/yr; AU ≈ 60,000–100,000.
Adoption model (Estimate, if adopters check all TMPs as WTGTM scenario): per customer 8 × $314.10 × 12 + $599.40 ≈ $30,750/yr.
| WA adoption of 60 firms | Customers | Revenue/yr |
|---|---|---|
| 10% | 6 | ≈ $185k |
| 25% | 15 | ≈ $461k |
| 50% | 30 | ≈ $923k |
Open question: whether customers check every TMP or only complex ones.
Answer (Owner, 2026-11-25): WTGTM intends to check **all** 8 TMPs/month. Model A (all-TMP adoption) adopted as base case for forecasting; Model B retained as downside. PROVISIONAL — single-customer evidence.

## MKT-04 — firm-size segmentation (2026-11-25)
WTGTM is a 1-person business (Owner fact) → 8 TMPs/month is a small-firm benchmark, not an average. Hypothesis (unverified) mix of 60 WA TMCs and volume: small 50% (30 firms, ~8/mo), medium 35% (21, ~30/mo), large 15% (9, ~100/mo) → weighted ≈ 30/mo/firm; WA ≈ 20,000–25,000 TMPs/yr incl. councils/utilities.
| Segment | Likely plan | $/month per customer | Adoption (Estimate) | Customers | Revenue/yr |
|---|---|---|---|---|---|
| Small (~8/mo) | Professional | $2,392 | 25% | 8 | ≈ $230k |
| Medium (~30/mo) | Business ($3,995 + 15 × $269) | $8,030 | 15% | 3 | ≈ $289k |
| Large (~100/mo) | Enterprise (from $9,990 + 60 × ≤$249.75) | ≈ $24,975 | 10% | 1 | ≈ $300k |
| Total | | | | ≈ 12 | ≈ $819k |
Small 1-person firms are the strongest fit (no in-house peer reviewer). Large firms may have in-house checking and check only complex TMPs. Validate firm-size mix against the Main Roads list.

## MKT-05 — WA firm-size investigation (2026-11-25)
- Main Roads registered list, "Traffic Management Company" type: **56** entries extracted (earlier 60 was an AI count; 56 is the line-by-line extraction). 3 have interstate head offices (Woolloongabba, Narre Warren North, Bundoora); 20 carry "conditions applicable" (mostly 2026–27 new registrations).
- Firmographic sample (Firecrawl enrichment, 26 credits): Altus Traffic ≈380 staff (national); Carrington's 201–500; Contraflow ≈85. 2 matches rejected (NZ firms of same name); 5 not found (likely small).
- **Key finding (Verified fact):** WTGTM (Way to Go Traffic Management) is **not** on the registered list. Registration covers companies *implementing* TM on State roads (crews). 1-person TMP designers like WTGTM are a separate, unregistered population; their number is not published.
- Revised segmentation (Hypothesis): registered TMCs — large (100+) ~8–12, medium (20–100) ~20–25, small (<20) ~20–25, mostly with in-house designers; plus independent 1–2 person designers ~20–60 (unverified).
- Small-designer segment (best fit): 20–60 × 25% adoption = 5–15 customers × ≈$28.7k/yr (Professional, 8/mo) ≈ $143k–$430k/yr.
- Next validation: AWTM-accredited designer count from Main Roads (requires Owner approval to contact a third party); ask WTGTM how many independent designers it knows.

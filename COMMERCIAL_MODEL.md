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

# COMMERCIAL_MODEL — TMP Check

All prices AUD. Approved by Owner 2026-11-20 (DECISIONS A-02–A-06).

## Price list — v2 structure (Owner approved 2026-11-25, A-22). Base price set 2026-11-25 (A-23)
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

Ladder (per check): single $349 > 5-pack $331.55 > 10-pack $314.10 > Professional $299 > Business $266.33 > Enterprise ≤$249.75. Unused included checks do not roll over. Approved 2026-11-25 (A-24).

Superseded v1 (A-03–A-06): $149/check; 10-pack $1,341.

```yaml
pricing:
  base_check: 349.00        # A-23
  packs: {5: 0.05, 10: 0.10}
```

## Credit rules (approved)
1. Purchased upfront. 2. Added after successful payment. 3. 1 credit per completed check. 4. Failed upload/processing: no charge. 5. Correction of a TMP Check error: no charge. 6. Customer re-check after document changes: 1 credit. 7. Valid 12 months from purchase. 8. Balance and history visible to customer. 9. Subscription billed separately.

**Approved (A-30):** lapse = credits retained; cancel = unused credits forfeited. Consumption oldest-lot-first. **Pilot price (A-31):** $145/check for WTGTM during G7.

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
| AI processing | $2–$15 | Est. 80-page TMP + drawings; measure in prototype |
| Human review (pilot) | $0 to TMP Check — performed by customer's accredited reviewer (A-15) | Cost borne by customer; reduces their net saving |
| Hosting/storage | < $1 | Small-scale cloud |
| Payment fees | ~1.75%–2.9% + fixed | Provider TBD |

**Our contribution per credit (estimate):** ≈ $149 − AI/infra (~$3–16) − payment fees ≈ **$128–143**.

**Customer net saving per check (estimate):** $405 − $149 − (reviewer hrs × $75). At 1 hr review ≈ $181; at 2 hrs ≈ $106. Reviewer time remains a key metric because it drives the customer's value.

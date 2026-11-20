# COMMERCIAL_MODEL — TMP Check

All prices AUD. Approved by Owner 2026-11-20 (DECISIONS A-02–A-06).

## Price list
| SKU | Price | Notes |
|---|---|---|
| Monthly subscription | $49.95 | Platform access only; no credits included |
| 1 checking credit | $149.00 | 1 completed TMP check |
| 10-credit pack | $1,341.00 | 10% off $1,490; effective $134.10/credit; saves $149 |
| (5 credits) | $745.00 | = 5 × $149, no discount — SKU status pending P-05 |

## Credit rules (approved)
1. Purchased upfront. 2. Added after successful payment. 3. 1 credit per completed check. 4. Failed upload/processing: no charge. 5. Correction of a TMP Check error: no charge. 6. Customer re-check after document changes: 1 credit. 7. Valid 12 months from purchase. 8. Balance and history visible to customer. 9. Subscription billed separately.

**Pending (P-07):** behaviour on subscription lapse; refunds; consumption order (recommend oldest-lot-first).

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

**Measured 2026-11-20 (OWNER-FT-02):** AI processing US$3.33 for SU026 (61 pp, passes A–D) ≈ A$5. Within the $2–15 assumption.

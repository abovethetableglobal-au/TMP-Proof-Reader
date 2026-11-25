"""Admin ledger tools (A-48). Append-only: never edits or deletes ledger rows.

    python -m src.portal.admin refunds                       # refunds flagged by the Stripe webhook
    python -m src.portal.admin adjust --payment-ref cs_test_... --qty 5 --by "Admin name" --reason "Refund re_..."

`adjust` removes credits from the purchase lot paid by that Stripe Checkout session, by appending a
negative 'adjustment' row. It never removes more than the lot still holds (used credits stay used).
"""
import argparse
import sys

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import AuditEvent, CreditLedger, LedgerType, SessionLocal, init_db, utcnow


def flagged_refunds(db: Session) -> list[AuditEvent]:
    return db.execute(select(AuditEvent).where(AuditEvent.action == "stripe_refund_review")
                      .order_by(AuditEvent.at)).scalars().all()


def refund_adjust(db: Session, payment_ref: str, qty: int, by: str, reason: str) -> CreditLedger:
    if qty <= 0:
        raise ValueError("qty must be a positive number of credits to remove")
    if not by.strip() or not reason.strip():
        raise ValueError("--by and --reason are required")
    lot = db.execute(select(CreditLedger).where(CreditLedger.payment_ref == payment_ref,
                                                CreditLedger.type == LedgerType.purchase)).scalar_one_or_none()
    if lot is None:
        raise ValueError(f"No purchase found for {payment_ref}")
    remaining = db.execute(select(func.coalesce(func.sum(CreditLedger.qty), 0))
                           .where(CreditLedger.lot_id == lot.id)).scalar_one()
    if qty > remaining:
        raise ValueError(f"Lot has only {remaining} unused credit(s); cannot remove {qty}")
    row = CreditLedger(org_id=lot.org_id, lot_id=lot.id, type=LedgerType.adjustment, qty=-qty,
                       payment_ref=payment_ref, created_at=utcnow(), created_by=by, reason=f"Refund: {reason}")
    db.add(row)
    db.add(AuditEvent(org_id=lot.org_id, action="refund_adjustment", object=payment_ref,
                      detail=f"-{qty} by {by}: {reason}"))
    db.commit()
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("refunds")
    a = sp.add_parser("adjust")
    a.add_argument("--payment-ref", required=True); a.add_argument("--qty", type=int, required=True)
    a.add_argument("--by", required=True); a.add_argument("--reason", required=True)
    args = ap.parse_args()
    init_db()
    db = SessionLocal()
    if args.cmd == "refunds":
        rows = flagged_refunds(db)
        for r in rows:
            print(f"{r.at:%Y-%m-%d %H:%M}  org {r.org_id}  {r.object}  {r.detail}")
        print(f"{len(rows)} refund(s) flagged.")
        return
    try:
        row = refund_adjust(db, args.payment_ref, args.qty, args.by, args.reason)
    except ValueError as exc:
        sys.exit(str(exc))
    print(f"Recorded adjustment {row.qty} credit(s) on {args.payment_ref} (org {row.org_id}).")


if __name__ == "__main__":
    main()

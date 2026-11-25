"""Read models for portal pages. Every query is scoped to one organisation."""
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .db import Check, CheckStatus, CreditLedger, Finding, Organisation, utcnow

SEVERITIES = ["Critical", "Major", "Moderate", "Minor", "Query"]

STATUS_LABELS = {
    CheckStatus.uploaded: ("Uploaded", "neutral"),
    CheckStatus.processing: ("Processing", "info"),
    CheckStatus.draft_review: ("Draft — awaiting reviewer", "warn"),
    CheckStatus.final_issued: ("Final issued", "ok"),
    CheckStatus.failed: ("Failed — no credit used", "error"),
}


def _aware(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@dataclass
class CreditBalance:
    available: int
    next_expiry: datetime | None
    expiring_qty: int
    ever_purchased: bool


def credit_balance(db: Session, org_id: int, now: datetime | None = None) -> CreditBalance:
    """Derive balance from the append-only ledger.

    Remaining per lot = Σ qty of rows in that lot. A lot counts only while
    unexpired, so expiry needs no row to take effect.
    """
    now = now or utcnow()
    rows = db.execute(select(CreditLedger).where(CreditLedger.org_id == org_id)).scalars().all()
    lots: dict[int, int] = {}
    expiry: dict[int, datetime] = {}
    for r in rows:
        lot = r.lot_id if r.lot_id is not None else r.id
        lots[lot] = lots.get(lot, 0) + r.qty
        if r.type.value == "purchase":
            expiry[lot] = _aware(r.expires_at)
    usable = {lot: q for lot, q in lots.items()
              if q > 0 and lot in expiry and expiry[lot] and expiry[lot] > now}
    next_lot = min(usable, key=lambda lot: expiry[lot]) if usable else None
    return CreditBalance(
        available=sum(usable.values()),
        next_expiry=expiry[next_lot] if next_lot else None,
        expiring_qty=usable[next_lot] if next_lot else 0,
        ever_purchased=bool(expiry),
    )


def finding_counts(db: Session, check_ids: list[int]) -> dict[int, Counter]:
    if not check_ids:
        return {}
    out: dict[int, Counter] = {cid: Counter() for cid in check_ids}
    q = (select(Finding.check_id, Finding.severity, func.count())
         .where(Finding.check_id.in_(check_ids))
         .group_by(Finding.check_id, Finding.severity))
    for cid, sev, n in db.execute(q):
        out[cid][sev] = n
    return out


def findings_summary(c: Counter, status: CheckStatus) -> str:
    if status in (CheckStatus.uploaded, CheckStatus.processing, CheckStatus.failed):
        return "—"
    parts = [f"{c[s]} {s}" for s in SEVERITIES if c[s]]
    return ", ".join(parts) if parts else "No issue identified in this check"


def recent_checks(db: Session, org_id: int, limit: int = 5) -> list[dict]:
    checks = db.execute(select(Check).where(Check.org_id == org_id)
                        .order_by(Check.created_at.desc()).limit(limit)).scalars().all()
    counts = finding_counts(db, [c.id for c in checks])
    rows = []
    for c in checks:
        label, tone = STATUS_LABELS[c.status]
        rows.append({
            "id": c.id, "date": _aware(c.created_at), "doc_ref": c.doc_ref,
            "status": label, "tone": tone,
            "findings": findings_summary(counts.get(c.id, Counter()), c.status),
            "has_report": c.status in (CheckStatus.draft_review, CheckStatus.final_issued),
            "seconds": c.processing_seconds,
            "link": True,
        })
    return rows


def dashboard(db: Session, org: Organisation, now: datetime | None = None) -> dict:
    now = now or utcnow()
    bal = credit_balance(db, org.id, now)

    final = select(Check).where(Check.org_id == org.id, Check.status == CheckStatus.final_issued)
    completed = len(db.execute(final).scalars().all())
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month = sum(1 for c in db.execute(final).scalars()
                     if _aware(c.final_issued_at) and _aware(c.final_issued_at) >= month_start)

    awaiting = len(db.execute(select(Check.id).where(
        Check.org_id == org.id, Check.status == CheckStatus.draft_review)).all())

    return {
        "credits": bal,
        "subscription": {"status": org.subscription_status.value},
        "checks_completed": completed,
        "checks_this_month": this_month,
        "awaiting_review": awaiting,
        "recent": recent_checks(db, org.id),
    }


LEDGER_LABELS = {"purchase": "Credits purchased", "consume": "Credit used", "reversal": "Credit returned",
                 "expiry": "Credits expired", "adjustment": "Adjustment"}


def ledger_history(db: Session, org_id: int) -> list[dict]:
    rows = db.execute(select(CreditLedger, Check.doc_ref)
                      .outerjoin(Check, Check.id == CreditLedger.check_id)
                      .where(CreditLedger.org_id == org_id)
                      .order_by(CreditLedger.created_at.desc(), CreditLedger.id.desc())).all()
    return [{"date": _aware(r.created_at), "type": LEDGER_LABELS[r.type.value], "qty": r.qty,
             "ref": doc_ref or r.payment_ref or "", "expires": _aware(r.expires_at) if r.type.value == "purchase" else None,
             "reason": r.reason or ""} for r, doc_ref in rows]

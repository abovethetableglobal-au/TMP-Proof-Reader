"""Read models for portal pages. Every query is scoped to one organisation."""
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import settings
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
        })
    return rows


def dashboard(db: Session, org: Organisation, now: datetime | None = None) -> dict:
    now = now or utcnow()
    cfg = settings()
    bal = credit_balance(db, org.id, now)

    final = select(Check).where(Check.org_id == org.id, Check.status == CheckStatus.final_issued)
    completed = len(db.execute(final).scalars().all())
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    this_month = sum(1 for c in db.execute(final).scalars()
                     if _aware(c.final_issued_at) and _aware(c.final_issued_at) >= month_start)

    savings = None
    if org.savings_baseline_aud is not None and completed:
        # Estimate only (P-16): agreed baseline per check minus single-credit price,
        # for checks whose final report has been issued.
        per_check = float(org.savings_baseline_aud) - cfg["credit_products"][0]["price"]
        savings = max(per_check, 0) * completed

    return {
        "credits": bal,
        "subscription": {"status": org.subscription_status.value,
                         "price": cfg["subscription"]["price"]},
        "checks_completed": completed,
        "checks_this_month": this_month,
        "savings": savings,
        "savings_baseline_set": org.savings_baseline_aud is not None,
        "recent": recent_checks(db, org.id),
    }

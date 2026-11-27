"""Operator Console services (A-52): customers, credits, work queue, turnaround.

The TMP Check business (operator) runs checks for customer organisations. Credit changes are
append-only ledger rows with the operator's name and a reason (A-06, CLAUDE.md §5).
"""
from __future__ import annotations

from collections import Counter
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import services
from .auth import hash_password
from .config import settings
from .db import Check, CheckStatus, CreditLedger, LedgerType, Organisation, User, utcnow

OPEN = (CheckStatus.uploaded, CheckStatus.processing, CheckStatus.draft_review)


class OperatorError(ValueError):
    pass


# ---------- turnaround ----------
def _tt():
    t = settings()["turnaround"]
    tz = ZoneInfo(t["timezone"])
    hh, mm = map(int, t["cutoff"].split(":"))
    rh, rm = map(int, t["return_by"].split(":"))
    holidays = {date.fromisoformat(str(d)) for d in (t.get("holidays") or [])}
    return tz, time(hh, mm), time(rh, rm), set(t["business_days"]), holidays


def is_business_day(d: date) -> bool:
    _, _, _, days, holidays = _tt()
    return d.weekday() in days and d not in holidays


def batch_date(received: datetime) -> date:
    """The business day whose cut-off batch picks up a TMP received at `received`."""
    tz, cutoff, _, _, _ = _tt()
    local = received.astimezone(tz) if received.tzinfo else received.replace(tzinfo=ZoneInfo("UTC")).astimezone(tz)
    d = local.date()
    if is_business_day(d) and local.time() <= cutoff:
        return d
    d += timedelta(days=1)
    while not is_business_day(d):
        d += timedelta(days=1)
    return d


def due_at(received: datetime) -> datetime:
    tz, _, return_by, _, _ = _tt()
    return datetime.combine(batch_date(received), return_by, tzinfo=tz)


# ---------- customers ----------
def customers(db: Session, now: datetime | None = None) -> list[dict]:
    now = now or utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    orgs = db.execute(select(Organisation).where(Organisation.is_operator.isnot(True))
                      .order_by(Organisation.name)).scalars().all()
    rows = []
    for o in orgs:
        checks = db.execute(select(Check.status, Check.created_at).where(Check.org_id == o.id)).all()
        rows.append({
            "org": o,
            "credits": services.credit_balance(db, o.id, now).available,
            "open": sum(1 for s, _ in checks if s in OPEN),
            "month": sum(1 for _, c in checks if services._aware(c) >= month_start),
            "total": len(checks),
            "reviewers": db.execute(select(func.count()).select_from(User).where(
                User.org_id == o.id, User.role == "customer_reviewer", User.active.is_(True))).scalar_one(),
        })
    return rows


def create_customer(db: Session, name: str, **fields) -> Organisation:
    name = (name or "").strip()
    if not name:
        raise OperatorError("Enter the customer's name.")
    if db.execute(select(Organisation).where(func.lower(Organisation.name) == name.lower())).scalar_one_or_none():
        raise OperatorError("A customer with that name already exists.")
    org = Organisation(name=name[:200], status="active")
    update_customer(org, **fields)
    db.add(org)
    db.flush()
    return org


def update_customer(org: Organisation, **fields) -> None:
    for k in ("legal_name", "abn", "billing_contact", "billing_email", "phone", "notes"):
        if k in fields:
            v = (fields[k] or "").strip()
            setattr(org, k, v or None)
    if fields.get("abn"):
        digits = "".join(ch for ch in fields["abn"] if ch.isdigit())
        if len(digits) != 11:
            raise OperatorError("An ABN has 11 digits.")
        org.abn = f"{digits[:2]} {digits[2:5]} {digits[5:8]} {digits[8:]}"
    if fields.get("status"):
        if fields["status"] not in ("active", "paused", "closed"):
            raise OperatorError("Unknown status.")
        org.status = fields["status"]


def add_user(db: Session, org: Organisation, name: str, email: str, role: str, password: str) -> User:
    name, email = (name or "").strip(), (email or "").strip().lower()
    if not name or "@" not in email:
        raise OperatorError("Enter the person's name and email address.")
    if role not in ("customer_user", "customer_reviewer"):
        raise OperatorError("Choose a role.")
    if db.execute(select(User).where(func.lower(User.email) == email)).scalar_one_or_none():
        raise OperatorError("That email address is already in use.")
    try:
        pw = hash_password(password or "")
    except ValueError as e:
        raise OperatorError(str(e)) from e
    u = User(org_id=org.id, name=name[:200], email=email, role=role, password_hash=pw)
    db.add(u)
    db.flush()
    return u


# ---------- credits (append-only) ----------
def grant_credits(db: Session, org: Organisation, qty: int, by: str, reason: str, payment_ref: str = "") -> CreditLedger:
    if qty <= 0 or qty > 1000:
        raise OperatorError("Enter a number of credits between 1 and 1000.")
    if not reason.strip():
        raise OperatorError("A reason is required for every credit change.")
    months = int(settings()["credits"]["validity_months"])
    now = utcnow()
    row = CreditLedger(org_id=org.id, type=LedgerType.purchase, qty=qty, created_by=by,
                       reason=reason.strip(), payment_ref=(payment_ref or "").strip() or None,
                       expires_at=now + timedelta(days=round(months * 365 / 12)))
    db.add(row)
    db.flush()
    row.lot_id = row.id
    return row


def remove_credits(db: Session, org: Organisation, qty: int, by: str, reason: str) -> list[CreditLedger]:
    """Negative 'adjustment' rows against usable lots, soonest-expiring first. Never below zero."""
    if qty <= 0:
        raise OperatorError("Enter a positive number of credits to remove.")
    if not reason.strip():
        raise OperatorError("A reason is required for every credit change.")
    now = utcnow()
    lots: dict[int, int] = {}
    expiry: dict[int, datetime] = {}
    for r in db.execute(select(CreditLedger).where(CreditLedger.org_id == org.id)).scalars():
        lot = r.lot_id if r.lot_id is not None else r.id
        lots[lot] = lots.get(lot, 0) + r.qty
        if r.type == LedgerType.purchase:
            expiry[lot] = services._aware(r.expires_at)
    usable = sorted((expiry[l], l, q) for l, q in lots.items() if q > 0 and expiry.get(l) and expiry[l] > now)
    if sum(q for _, _, q in usable) < qty:
        raise OperatorError(f"The customer has only {sum(q for _, _, q in usable)} usable credit(s).")
    rows, left = [], qty
    for _, lot, q in usable:
        take = min(q, left)
        rows.append(CreditLedger(org_id=org.id, lot_id=lot, type=LedgerType.adjustment, qty=-take,
                                 created_by=by, reason=reason.strip()))
        left -= take
        if not left:
            break
    db.add_all(rows)
    db.flush()
    return rows


# ---------- work queue ----------
def queue(db: Session, include_done_days: int = 7, now: datetime | None = None) -> list[dict]:
    now = now or utcnow()
    since = now - timedelta(days=include_done_days)
    rows = db.execute(select(Check, Organisation.name).join(Organisation, Organisation.id == Check.org_id)
                      .where((Check.status.in_(OPEN)) | (Check.created_at >= since))
                      .order_by(Check.created_at)).all()
    counts = services.finding_counts(db, [c.id for c, _ in rows])
    out = []
    for c, org_name in rows:
        received = services._aware(c.created_at)
        due = due_at(received)
        label, tone = services.STATUS_LABELS[c.status]
        done = services._aware(c.final_issued_at)
        out.append({
            "check": c, "customer": org_name, "received": received, "due": due, "status": label, "tone": tone,
            "open": c.status in OPEN,
            "overdue": c.status in OPEN and now > due,
            "late": bool(done and done > due),
            "findings": services.findings_summary(counts.get(c.id, Counter()), c.status),
            "cost": c.ai_cost_usd or "",
        })
    out.sort(key=lambda r: (not r["open"], r["due"]))
    return out

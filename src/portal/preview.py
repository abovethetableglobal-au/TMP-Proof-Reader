"""Hosted pilot preview (Owner approval 2026-11-26, A-53): a limited G6 exception for invited reviewers.

TMPCHECK_ENV=preview enables it. Conditions enforced here and in app/processing:
- invite-only self sign-up (TMPCHECK_INVITES), reviewer profile with accreditation details;
- every upload must be confirmed as historical or anonymised (no live customer TMPs);
- AI spend cap per calendar month (ai.monthly_cap_usd): above it checks run rules only;
- HTTPS cookies and an explicit session secret are required.
"""
import os
from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import settings
from .db import Check, CreditLedger, LedgerType, Organisation, User, utcnow


def env() -> str:
    return os.environ.get("TMPCHECK_ENV", "")


def is_preview() -> bool:
    return env() == "preview"


def startup_guard() -> None:
    if env() == "local":
        return
    if env() != "preview":
        raise RuntimeError("Set TMPCHECK_ENV=local (PC) or TMPCHECK_ENV=preview (approved hosted pilot preview, A-53).")
    missing = [n for n in ("TMPCHECK_SECRET", "TMPCHECK_INVITES") if not os.environ.get(n)]
    if os.environ.get("TMPCHECK_HTTPS") != "1":
        missing.append("TMPCHECK_HTTPS=1")
    if missing:
        raise RuntimeError("Preview needs: " + ", ".join(missing))


def invites() -> dict[str, dict]:
    """TMPCHECK_INVITES = 'CODE|Organisation name|credits;CODE2|…'. Codes are case-sensitive secrets."""
    out = {}
    for part in (os.environ.get("TMPCHECK_INVITES") or "").split(";"):
        bits = [b.strip() for b in part.split("|")]
        if len(bits) == 3 and bits[0]:
            out[bits[0]] = {"org": bits[1], "credits": int(bits[2] or 0)}
    return out


class SignupError(ValueError):
    pass


def signup(db: Session, code: str, name: str, email: str, password: str,
           level: str, number: str, expiry: str) -> User:
    from .auth import hash_password
    inv = invites().get(code or "")
    if not inv:
        raise SignupError("This invite code is not valid. Check the link you were sent.")
    email = (email or "").strip().lower()
    if not name.strip() or "@" not in email:
        raise SignupError("Enter your name and a valid email address.")
    if not (level.strip() and number.strip() and expiry.strip()):
        raise SignupError("Enter your accreditation level, number and expiry. Reviewers must be accredited.")
    if db.execute(select(User).where(func.lower(User.email) == email)).scalar_one_or_none():
        raise SignupError("An account with this email already exists. Sign in instead.")
    pw = hash_password(password)          # raises ValueError if too short
    org = db.execute(select(Organisation).where(Organisation.name == inv["org"])).scalar_one_or_none()
    if org is None:
        org = Organisation(name=inv["org"]); db.add(org); db.flush()
    user = User(org_id=org.id, name=name.strip()[:200], email=email, role="customer_reviewer", password_hash=pw,
                accreditation_level=level.strip()[:60], accreditation_number=number.strip()[:60],
                accreditation_expiry=expiry.strip()[:20])
    db.add(user)
    ref = f"INVITE-{code}"
    if inv["credits"] > 0 and not db.execute(select(CreditLedger.id).where(
            CreditLedger.org_id == org.id, CreditLedger.payment_ref == ref)).first():
        now = utcnow()
        lot = CreditLedger(org_id=org.id, type=LedgerType.purchase, qty=inv["credits"], payment_ref=ref,
                           created_at=now, expires_at=now + timedelta(days=365), created_by="invite",
                           reason="Pilot preview test credits (no charge)")
        db.add(lot); db.flush(); lot.lot_id = lot.id
    db.commit()
    return user


def month_ai_spend(db: Session) -> float:
    start = utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    vals = db.execute(select(Check.ai_cost_usd).where(Check.created_at >= start)).scalars().all()
    total = 0.0
    for v in vals:
        try:
            total += float(v or 0)
        except ValueError:
            pass
    return total


def ai_cap_reached(db: Session) -> tuple[bool, str]:
    cap = (settings().get("ai") or {}).get("monthly_cap_usd")
    if cap is None:
        return False, ""
    spent = month_ai_spend(db)
    if spent >= float(cap):
        return True, f"monthly AI spend cap reached (US${spent:.2f} of US${float(cap):.2f}); rule checks only"
    return False, ""

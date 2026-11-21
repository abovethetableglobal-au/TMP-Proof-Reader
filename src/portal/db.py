"""Portal data model (SQLite locally; Postgres from G6 — ARCHITECTURE Stage 2).

Every customer-owned table carries ``org_id``; all queries go through
``services`` helpers that filter on it (tenant separation, brief §7).
"""
import enum
import os
from datetime import datetime, timezone

from sqlalchemy import (Enum, ForeignKey, Integer, String, Text,
                        DateTime, create_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from .config import ROOT


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class SubscriptionStatus(str, enum.Enum):
    none = "none"
    active = "active"
    lapsed = "lapsed"
    cancelled = "cancelled"


class CheckStatus(str, enum.Enum):
    """Statuses shown to customers. A check is never 'completed' before the
    accredited reviewer has dispositioned every finding (A-15)."""
    uploaded = "uploaded"
    processing = "processing"
    draft_review = "draft_review"      # draft with customer's accredited reviewer
    final_issued = "final_issued"      # reviewer dispositioned all findings
    failed = "failed"                  # no credit consumed (A-05 rule 4)


class LedgerType(str, enum.Enum):
    purchase = "purchase"
    consume = "consume"
    reversal = "reversal"
    expiry = "expiry"
    adjustment = "adjustment"


class Organisation(Base):
    __tablename__ = "organisation"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    subscription_status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus), default=SubscriptionStatus.none)
    subscription_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    role: Mapped[str] = mapped_column(String(32), default="customer_user")   # customer_user | customer_reviewer | admin
    password_hash: Mapped[str | None] = mapped_column(String(300))
    active: Mapped[bool] = mapped_column(default=True)


class UserSession(Base):
    """Server-side login session. Only a hash of the cookie token is stored."""
    __tablename__ = "user_session"
    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AuditEvent(Base):
    """Append-only access and action log (brief §7, ARCHITECTURE security baseline)."""
    __tablename__ = "audit_event"
    id: Mapped[int] = mapped_column(primary_key=True)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    org_id: Mapped[int | None] = mapped_column(Integer, index=True)
    user_id: Mapped[int | None] = mapped_column(Integer)
    action: Mapped[str] = mapped_column(String(60))
    object: Mapped[str | None] = mapped_column(String(120))
    detail: Mapped[str | None] = mapped_column(Text)
    ip: Mapped[str | None] = mapped_column(String(64))


class Check(Base):
    __tablename__ = "tmp_check"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"), index=True)
    doc_ref: Mapped[str] = mapped_column(String(200))
    filename: Mapped[str] = mapped_column(String(300))
    status: Mapped[CheckStatus] = mapped_column(Enum(CheckStatus), default=CheckStatus.uploaded)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    final_issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewer_name: Mapped[str | None] = mapped_column(String(200))   # who issued the final (A-15)
    failure_reason: Mapped[str | None] = mapped_column(Text)
    pages: Mapped[int | None] = mapped_column(Integer)
    storage_path: Mapped[str | None] = mapped_column(String(500))
    ai_passes: Mapped[str | None] = mapped_column(String(300))      # e.g. "A,B,C" when AI checks ran
    ai_cost_usd: Mapped[str | None] = mapped_column(String(20))


class Finding(Base):
    __tablename__ = "finding"
    id: Mapped[int] = mapped_column(primary_key=True)
    check_id: Mapped[int] = mapped_column(ForeignKey("tmp_check.id"), index=True)
    severity: Mapped[str] = mapped_column(String(16))   # Critical|Major|Moderate|Minor|Query
    page: Mapped[int] = mapped_column(Integer)
    section: Mapped[str] = mapped_column(String(200))
    evidence: Mapped[str] = mapped_column(Text)
    issue: Mapped[str] = mapped_column(Text, default="")
    action: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(40), default="")
    outcome: Mapped[str] = mapped_column(String(40), default="Potential issue")
    rule: Mapped[str | None] = mapped_column(String(60))
    source: Mapped[str] = mapped_column(String(60), default="rules")  # which checks raised it, e.g. "AI C, rules"
    pages: Mapped[str | None] = mapped_column(String(300))      # all pages the issue affects, e.g. "10, 59, 60"
    disposition: Mapped[str] = mapped_column(String(16), default="pending")   # pending|accepted|edited|rejected
    reviewer_note: Mapped[str | None] = mapped_column(Text)
    dispositioned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class CreditLedger(Base):
    """Append-only. Balances are derived (CLAUDE.md §5). Never UPDATE or DELETE rows."""
    __tablename__ = "credit_ledger"
    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"), index=True)
    lot_id: Mapped[int | None] = mapped_column(Integer, index=True)  # purchase row id
    type: Mapped[LedgerType] = mapped_column(Enum(LedgerType))
    qty: Mapped[int] = mapped_column(Integer)
    check_id: Mapped[int | None] = mapped_column(ForeignKey("tmp_check.id"))
    payment_ref: Mapped[str | None] = mapped_column(String(200))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    created_by: Mapped[str] = mapped_column(String(200))
    reason: Mapped[str | None] = mapped_column(Text)


DB_URL = os.environ.get("TMPCHECK_DB_URL", f"sqlite:///{ROOT / 'output' / 'portal.db'}")


def make_engine(url: str = DB_URL):
    if url.startswith("sqlite:///"):
        (ROOT / "output").mkdir(exist_ok=True)
    return create_engine(url)


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db(eng=None) -> None:
    eng = eng or engine
    Base.metadata.create_all(eng)
    _add_missing_columns(eng)


def _add_missing_columns(eng) -> None:
    """Local SQLite only: add columns introduced after a database was created (no data is changed)."""
    if eng.dialect.name != "sqlite":
        return
    from sqlalchemy import inspect, text
    insp = inspect(eng)
    with eng.begin() as conn:
        for table in Base.metadata.sorted_tables:
            have = {c["name"] for c in insp.get_columns(table.name)}
            for col in table.columns:
                if col.name not in have:
                    default = ""
                    if col.default is not None and getattr(col.default, "is_scalar", False):
                        v = col.default.arg
                        default = f" DEFAULT {int(v) if isinstance(v, bool) else repr(v)}"
                    conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" '
                                      f'{col.type.compile(dialect=eng.dialect)}{default}'))

"""Stripe sandbox integration (DECISIONS A-46, Option A).

Test mode only until Gate 5 (A-09): the key must be a ``sk_test_`` key and
``stripe.mode`` must be ``test``. Live keys are refused.

Flow: the billing page starts a Stripe Checkout session; Stripe calls the
webhook; the webhook appends a ``purchase`` row to the append-only credit
ledger (credits) or sets the organisation's subscription status. Prices come
from ``config/portal.yaml`` (CLAUDE.md §5), sent as ``price_data``.
"""
import os
from datetime import timedelta

import stripe
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .db import CreditLedger, LedgerType, Organisation, SubscriptionStatus, utcnow
from . import auth


class PaymentsUnavailable(RuntimeError):
    pass


def _cfg() -> dict:
    return settings().get("stripe", {}) or {}


def secret_key() -> str | None:
    return os.environ.get("STRIPE_SECRET_KEY")


def sandbox_enabled() -> bool:
    """True only for an enabled test-mode config with a test key present."""
    c = _cfg()
    key = secret_key() or ""
    return bool(c.get("sandbox_enabled")) and c.get("mode") == "test" and key.startswith("sk_test_")


def _client() -> stripe.StripeClient:
    key = secret_key() or ""
    if _cfg().get("mode") != "test" or not key.startswith("sk_test_"):
        raise PaymentsUnavailable("Stripe is test mode only before Gate 5 (A-09). Use an sk_test_ key.")
    if not _cfg().get("sandbox_enabled"):
        raise PaymentsUnavailable("Stripe sandbox is not enabled in config/portal.yaml.")
    return stripe.StripeClient(key)


def _cents(amount: float) -> int:
    return int(round(amount * 100))


def product(sku: str) -> dict | None:
    cfg = settings()
    if sku == cfg["subscription"]["sku"]:
        return cfg["subscription"]
    return next((p for p in cfg["credit_products"] if p["sku"] == sku and p["offered"]), None)


def _customer(client: stripe.StripeClient, db: Session, org: Organisation, email: str) -> str:
    if org.stripe_customer_id:
        return org.stripe_customer_id
    cust = client.v1.customers.create(params={"name": org.name, "email": email,
                                              "metadata": {"org_id": str(org.id)}})
    org.stripe_customer_id = cust.id
    db.commit()
    return cust.id


def create_checkout(db: Session, org: Organisation, email: str, sku: str, base_url: str) -> str:
    """Create a Checkout session and return its URL."""
    p = product(sku)
    if p is None:
        raise ValueError(f"Unknown product {sku}")
    client = _client()
    cfg = settings()
    currency = cfg["currency"].lower()
    meta = {"org_id": str(org.id), "sku": sku}
    is_sub = sku == cfg["subscription"]["sku"]
    price_data = {"currency": currency, "unit_amount": _cents(p["price"]),
                  "product_data": {"name": f"TMP Check — {p['name']}"}}
    if is_sub:
        price_data["recurring"] = {"interval": p["interval"]}
    params = {
        "mode": "subscription" if is_sub else "payment",
        "customer": _customer(client, db, org, email),
        "line_items": [{"price_data": price_data, "quantity": 1}],
        "metadata": meta,
        "client_reference_id": str(org.id),
        "success_url": f"{base_url}/billing?paid=1",
        "cancel_url": f"{base_url}/billing?cancelled=1",
        # Managed Payments (Stripe as merchant of record) is an Owner tax/commercial decision; off until decided.
        "managed_payments": {"enabled": bool(_cfg().get("managed_payments", False))},
    }
    if is_sub:
        params["subscription_data"] = {"metadata": meta}
    else:
        params["payment_intent_data"] = {"metadata": meta}
        params["invoice_creation"] = {"enabled": True}
    session = client.v1.checkout.sessions.create(params=params)
    return session.url


def parse_event(payload: bytes, sig_header: str | None):
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    if not secret:
        raise PaymentsUnavailable("STRIPE_WEBHOOK_SECRET is not set.")
    return stripe.Webhook.construct_event(payload, sig_header or "", secret)


def _org(db: Session, meta: dict | None) -> Organisation | None:
    try:
        return db.get(Organisation, int((meta or {}).get("org_id")))
    except (TypeError, ValueError):
        return None


SUB_STATUS = {"active": SubscriptionStatus.active, "trialing": SubscriptionStatus.active,
              "past_due": SubscriptionStatus.lapsed, "unpaid": SubscriptionStatus.lapsed,
              "incomplete_expired": SubscriptionStatus.lapsed, "canceled": SubscriptionStatus.cancelled}


def handle_event(db: Session, event) -> str:
    """Apply one webhook event. Idempotent: a session already in the ledger is skipped."""
    etype, obj = event["type"], event["data"]["object"]
    if event.get("livemode"):
        return "ignored: live-mode event before G5"

    if etype in ("checkout.session.completed", "checkout.session.async_payment_succeeded"):
        if obj.get("mode") != "payment" or obj.get("payment_status") != "paid":
            return "ignored: not a paid one-off payment"
        org, p = _org(db, obj.get("metadata")), product((obj.get("metadata") or {}).get("sku", ""))
        if org is None or p is None or "credits" not in p:
            return "ignored: unknown org or product"
        if obj.get("amount_total") != _cents(p["price"]):
            auth.audit(db, None, "stripe_amount_mismatch", obj["id"], f"{obj.get('amount_total')}", org_id=org.id)
            return "held: amount mismatch"
        exists = db.execute(select(CreditLedger.id).where(CreditLedger.payment_ref == obj["id"])).first()
        if exists:
            return "duplicate"
        now = utcnow()
        row = CreditLedger(org_id=org.id, type=LedgerType.purchase, qty=p["credits"], payment_ref=obj["id"],
                           created_at=now, created_by="stripe:test",
                           expires_at=now + timedelta(days=round(365 * settings()["credits"]["validity_months"] / 12)),
                           reason=f"{p['name']} (Stripe test mode)")
        db.add(row); db.flush(); row.lot_id = row.id; db.commit()
        auth.audit(db, None, "stripe_credit_purchase", obj["id"], p["sku"], org_id=org.id)
        return "credited"

    if etype in ("customer.subscription.created", "customer.subscription.updated", "customer.subscription.deleted"):
        org = _org(db, obj.get("metadata"))
        if org is None:
            return "ignored: unknown org"
        status = SubscriptionStatus.cancelled if etype.endswith("deleted") else SUB_STATUS.get(obj.get("status"))
        if status is None:
            return "ignored: status " + str(obj.get("status"))
        if status == SubscriptionStatus.active and org.subscription_status != SubscriptionStatus.active:
            org.subscription_started_at = utcnow()
        org.subscription_status = status
        db.commit()
        auth.audit(db, None, "stripe_subscription", obj["id"], status.value, org_id=org.id)
        return "subscription " + status.value

    if etype == "charge.refunded":
        # Refunds never auto-remove credits: an admin reviews and records a ledger adjustment.
        org = _org(db, obj.get("metadata"))
        auth.audit(db, None, "stripe_refund_review", obj["id"], str(obj.get("amount_refunded")),
                   org_id=org.id if org else None)
        return "refund flagged for admin"

    return "ignored"

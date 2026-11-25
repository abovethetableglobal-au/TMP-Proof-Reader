"""A-46 Stripe sandbox: test-mode guard, webhook → append-only ledger, idempotency, subscriptions."""
import json
import os
import time

import pytest
import stripe

os.environ["TMPCHECK_ENV"] = "local"
os.environ.setdefault("TMPCHECK_DB_URL", "sqlite://")

from sqlalchemy import select

from src.portal import db as dbm, payments, services
from tests.portal.test_portal import db  # noqa: F401  (fixture)


def ev(etype, obj, live=False):
    return {"type": etype, "livemode": live, "data": {"object": obj}}


def paid_session(sid="cs_test_1", sku="CR-5", amount=165775, org="1"):
    return {"id": sid, "mode": "payment", "payment_status": "paid", "amount_total": amount,
            "metadata": {"org_id": org, "sku": sku}}


def test_live_key_refused(monkeypatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_live_abc")
    assert not payments.sandbox_enabled()
    with pytest.raises(payments.PaymentsUnavailable):
        payments._client()


def test_test_key_enables_sandbox(monkeypatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_abc")
    assert payments.sandbox_enabled()
    monkeypatch.delenv("STRIPE_SECRET_KEY")
    assert not payments.sandbox_enabled()


def test_paid_session_credits_once(db):
    assert payments.handle_event(db, ev("checkout.session.completed", paid_session())) == "credited"
    assert payments.handle_event(db, ev("checkout.session.completed", paid_session())) == "duplicate"
    b = services.credit_balance(db, 1)
    assert b.available == 5
    row = db.execute(select(dbm.CreditLedger)).scalar_one()
    assert row.lot_id == row.id and row.payment_ref == "cs_test_1"
    assert services.credit_balance(db, 2).available == 0      # tenant scoping


def test_unpaid_mismatch_and_live_ignored(db):
    s = paid_session(); s["payment_status"] = "unpaid"
    assert payments.handle_event(db, ev("checkout.session.completed", s)).startswith("ignored")
    assert payments.handle_event(db, ev("checkout.session.completed", paid_session(amount=100))) == "held: amount mismatch"
    assert payments.handle_event(db, ev("checkout.session.completed", paid_session(), live=True)).startswith("ignored")
    assert services.credit_balance(db, 1).available == 0


def test_subscription_lifecycle(db):
    sub = {"id": "sub_test", "status": "active", "metadata": {"org_id": "1", "sku": "SUB-MONTHLY"}}
    payments.handle_event(db, ev("customer.subscription.created", sub))
    org = db.get(dbm.Organisation, 1)
    assert org.subscription_status == dbm.SubscriptionStatus.active and org.subscription_started_at
    payments.handle_event(db, ev("customer.subscription.updated", {**sub, "status": "past_due"}))
    assert org.subscription_status == dbm.SubscriptionStatus.lapsed
    payments.handle_event(db, ev("customer.subscription.deleted", sub))
    assert org.subscription_status == dbm.SubscriptionStatus.cancelled


def test_refund_does_not_remove_credits(db):
    payments.handle_event(db, ev("checkout.session.completed", paid_session()))
    assert payments.handle_event(db, ev("charge.refunded", {"id": "ch_1", "amount_refunded": 165775,
                                                             "metadata": {"org_id": "1"}})) == "refund flagged for admin"
    assert services.credit_balance(db, 1).available == 5


def test_webhook_signature(monkeypatch):
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test")
    body = json.dumps(ev("ping", {})).encode()
    ts = int(time.time())
    sig = stripe.WebhookSignature._compute_signature(f"{ts}.{body.decode()}", "whsec_test")
    assert payments.parse_event(body, f"t={ts},v1={sig}")["type"] == "ping"
    with pytest.raises(Exception):
        payments.parse_event(body, f"t={ts},v1=bad")


def test_checkout_params(db, monkeypatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_abc")
    seen = {}

    class Fake:
        def __init__(self, key):
            self.v1 = self
            self.customers = self; self.checkout = self; self.sessions = self
        def create(self, params):
            if "line_items" in params:
                seen.update(params); return type("S", (), {"url": "https://checkout.stripe.com/x"})
            return type("C", (), {"id": "cus_test"})

    monkeypatch.setattr(payments.stripe, "StripeClient", Fake)
    org = db.get(dbm.Organisation, 1)
    assert payments.create_checkout(db, org, "a@x", "CR-1", "http://t") == "https://checkout.stripe.com/x"
    li = seen["line_items"][0]["price_data"]
    assert (seen["mode"], li["currency"], li["unit_amount"]) == ("payment", "aud", 34900)
    assert org.stripe_customer_id == "cus_test"
    payments.create_checkout(db, org, "a@x", "SUB-MONTHLY", "http://t")
    assert seen["mode"] == "subscription" and seen["line_items"][0]["price_data"]["recurring"] == {"interval": "month"}


def test_invalid_email_not_sent(db, monkeypatch):
    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_abc")
    sent = {}

    class Fake:
        def __init__(self, key):
            self.v1 = self; self.customers = self; self.checkout = self; self.sessions = self
        def create(self, params):
            if "line_items" in params:
                return type("S", (), {"url": "u"})
            sent.update(params); return type("C", (), {"id": "cus_x"})

    monkeypatch.setattr(payments.stripe, "StripeClient", Fake)
    payments.create_checkout(db, db.get(dbm.Organisation, 1), "stripe-test@localhost", "CR-1", "http://t")
    assert "email" not in sent


def test_real_signed_event_credits(db, monkeypatch):
    """Regression: a genuinely signed webhook (not a hand-made dict) must credit the ledger."""
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_test")
    body = json.dumps({"id": "evt_1", "object": "event", "type": "checkout.session.completed", "livemode": False,
                       "data": {"object": {**paid_session("cs_test_real"), "object": "checkout.session"}}}).encode()
    ts = int(time.time())
    sig = stripe.WebhookSignature._compute_signature(f"{ts}.{body.decode()}", "whsec_test")
    assert payments.handle_event(db, payments.parse_event(body, f"t={ts},v1={sig}")) == "credited"
    assert services.credit_balance(db, 1).available == 5

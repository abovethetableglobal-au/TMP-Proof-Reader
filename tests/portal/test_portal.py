"""Portal S1 tests: ledger derivation, empty states, no mock-up data, pricing, tenant scoping."""
import os
from datetime import datetime, timedelta, timezone

import pytest

os.environ["TMPCHECK_ENV"] = "local"
os.environ.setdefault("TMPCHECK_DB_URL", "sqlite://")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.portal import app as appmod, db as dbm, services
from src.portal.config import price_label, settings

NOW = datetime(2026, 11, 20, tzinfo=timezone.utc)


@pytest.fixture
def db():
    eng = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    dbm.Base.metadata.create_all(eng)
    S = sessionmaker(bind=eng, expire_on_commit=False)
    s = S()
    a = dbm.Organisation(name="Org A"); b = dbm.Organisation(name="Org B")
    s.add_all([a, b]); s.flush()
    from tests.portal.conftest import PW_HASH
    s.add_all([dbm.User(org_id=a.id, name="Alice Smith", email="a@x", role="customer_reviewer", password_hash=PW_HASH),
               dbm.User(org_id=b.id, name="Bob", email="b@x", password_hash=PW_HASH)])
    s.commit()
    yield s
    s.close()


def buy(s, org, qty, when, ref="INV"):
    r = dbm.CreditLedger(org_id=org, type=dbm.LedgerType.purchase, qty=qty, created_at=when,
                         expires_at=when + timedelta(days=365), created_by="admin", payment_ref=ref)
    s.add(r); s.flush(); r.lot_id = r.id; s.commit()
    return r


def test_balance_empty(db):
    b = services.credit_balance(db, 1, NOW)
    assert (b.available, b.next_expiry, b.ever_purchased) == (0, None, False)


def test_balance_consume_reversal_and_expiry(db):
    old = buy(db, 1, 10, NOW - timedelta(days=400))      # expired lot
    new = buy(db, 1, 10, NOW - timedelta(days=10))
    db.add_all([
        dbm.CreditLedger(org_id=1, lot_id=new.id, type=dbm.LedgerType.consume, qty=-1, created_by="sys"),
        dbm.CreditLedger(org_id=1, lot_id=new.id, type=dbm.LedgerType.consume, qty=-1, created_by="sys"),
        dbm.CreditLedger(org_id=1, lot_id=new.id, type=dbm.LedgerType.reversal, qty=1, created_by="admin",
                         reason="TMP Check error"),
    ]); db.commit()
    b = services.credit_balance(db, 1, NOW)
    assert b.available == 9 and b.ever_purchased
    assert b.next_expiry.date() == (NOW - timedelta(days=10) + timedelta(days=365)).date()


def test_balance_is_tenant_scoped(db):
    buy(db, 1, 10, NOW)
    assert services.credit_balance(db, 2, NOW).available == 0


def test_recent_checks_tenant_scoped_and_wording(db):
    c = dbm.Check(org_id=1, doc_ref="REF-A", filename="a.pdf", status=dbm.CheckStatus.draft_review)
    d = dbm.Check(org_id=2, doc_ref="REF-B", filename="b.pdf", status=dbm.CheckStatus.final_issued)
    db.add_all([c, d]); db.commit()
    rows = services.recent_checks(db, 1)
    assert [r["doc_ref"] for r in rows] == ["REF-A"]
    assert rows[0]["status"] == "Draft — awaiting reviewer"
    assert rows[0]["findings"] == "No issue identified in this check"


def test_completed_counts_final_only_and_awaiting_review(db):
    org = db.get(dbm.Organisation, 1)
    db.add_all([dbm.Check(org_id=1, doc_ref="X", filename="x", status=dbm.CheckStatus.draft_review),
                dbm.Check(org_id=1, doc_ref="Y", filename="y", status=dbm.CheckStatus.final_issued,
                          final_issued_at=NOW)]); db.commit()
    d = services.dashboard(db, org, NOW)
    assert d["checks_completed"] == 1 and d["checks_this_month"] == 1
    assert d["awaiting_review"] == 1


def test_prices_match_approved_commercial_model():
    cfg = settings()
    assert cfg["subscription"]["price"] == 49.95
    prices = {p["sku"]: p["price"] for p in cfg["credit_products"]}
    assert prices == {"CR-1": 349.0, "CR-5": 1657.75, "CR-10": 3141.0}
    assert cfg["payments_enabled"] is False          # A-09
    assert "GST-inclusive" not in price_label() and "incl" not in price_label()


@pytest.fixture
def client(db):
    from fastapi.testclient import TestClient
    appmod.app.dependency_overrides[appmod.get_db] = lambda: db
    from tests.portal.conftest import login
    with TestClient(appmod.app) as c:
        login(c, "a@x")
        yield c
    appmod.app.dependency_overrides.clear()


FORBIDDEN = ["2,659", "TMP-2025-0", "15 Apr 2026", "Way Too Go", "John Doe", "Compliant", "No Issues Found", "approved", "100%"]


@pytest.mark.parametrize("path", ["/", "/checks/new", "/checks", "/billing", "/library", "/help"])
def test_pages_render_without_mockup_data_or_forbidden_words(client, path):
    r = client.get(path)
    assert r.status_code == 200
    html = r.text
    for bad in FORBIDDEN:
        if path == "/library" and bad == "approved":
            continue
        assert bad not in html, f"{bad!r} on {path}"


def test_dashboard_empty_states(client):
    html = client.get("/").text
    assert "No credits purchased yet" in html
    assert "No checks yet" in html
    assert "Awaiting Review" in html and "Savings" not in html
    assert "Fast. Thorough. Evidence-based." in html
    assert "Org A" in html and "Org B" not in html


def test_five_pack_offered_a23(client):
    html = client.get("/billing").text
    assert "Five-credit pack" in html and "$1,657.75" in html


def test_library_lists_22_approved_rules(client):
    assert client.get("/library").text.count("<code>WA-") == 22

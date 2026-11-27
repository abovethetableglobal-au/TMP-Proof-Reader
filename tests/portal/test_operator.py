"""A-52 Operator Console: customers, credits, work queue, turnaround, checks on a customer's behalf."""
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from src.portal import db as dbm, operator, services
from tests.portal.conftest import PW_HASH, login
from tests.portal.test_workflow import SAMPLE, add_credits, env  # noqa: F401  (env is a fixture)

PERTH = ZoneInfo("Australia/Perth")


@pytest.fixture
def op(env):
    c, S = env
    with S() as s:
        o = dbm.Organisation(name="TMP Check", is_operator=True)
        s.add(o); s.flush()
        s.add(dbm.User(org_id=o.id, name="Owner", email="op@x", role="admin", password_hash=PW_HASH))
        s.commit()
    login(c, "op@x")
    return c, S


# ---------- turnaround rule ----------
@pytest.mark.parametrize("received, due", [
    (datetime(2026, 11, 26, 10, 0, tzinfo=PERTH), datetime(2026, 11, 26, 17, 0, tzinfo=PERTH)),   # Thu before cut-off
    (datetime(2026, 11, 26, 12, 30, tzinfo=PERTH), datetime(2026, 11, 26, 17, 0, tzinfo=PERTH)),  # exactly at cut-off
    (datetime(2026, 11, 26, 12, 31, tzinfo=PERTH), datetime(2026, 11, 27, 17, 0, tzinfo=PERTH)),  # after -> Fri
    (datetime(2026, 11, 27, 13, 0, tzinfo=PERTH), datetime(2026, 11, 30, 17, 0, tzinfo=PERTH)),   # Fri after -> Mon
    (datetime(2026, 11, 28, 9, 0, tzinfo=PERTH), datetime(2026, 11, 30, 17, 0, tzinfo=PERTH)),    # Sat -> Mon
])
def test_due_time(received, due):
    assert operator.due_at(received) == due


def test_holiday_skipped(monkeypatch):
    real = operator.settings
    def fake():
        cfg = real(); cfg["turnaround"]["holidays"] = ["2026-11-30"]; return cfg
    monkeypatch.setattr(operator, "settings", fake)
    assert operator.due_at(datetime(2026, 11, 27, 13, 0, tzinfo=PERTH)) == datetime(2026, 12, 1, 17, 0, tzinfo=PERTH)


# ---------- access ----------
def test_customers_cannot_see_operator_pages(env):
    c, S = env                                      # signed in as a customer reviewer
    for url in ("/admin/queue", "/admin/customers"):
        r = c.get(url)
        assert r.status_code == 403 and "Operator sign-in needed" in r.text and "Sign out and sign in as operator" in r.text
        assert "Work Queue</span>" not in r.text                  # operator menu still hidden
    assert c.post("/admin/customers", data={"name": "X"}).status_code == 404


def test_operator_nav_and_customer_list(op):
    c, S = op
    page = c.get("/admin/customers").text
    assert "Work Queue" in page and "Org A" in page and "Org B" in page
    with S() as s:
        names = [r["org"].name for r in operator.customers(s)]
    assert "TMP Check" not in names and "/admin/customers/3" not in page   # operator org is not a customer


# ---------- customers & people ----------
def test_create_customer_and_validation(op):
    c, S = op
    r = c.post("/admin/customers", data={"name": "Blackstone", "abn": "12 345 678 901", "billing_email": "ap@b.example"})
    assert "Customer created" in r.text and "Blackstone" in r.text
    assert "already exists" in c.post("/admin/customers", data={"name": "blackstone"}).text
    with S() as s:
        org = s.query(dbm.Organisation).filter_by(name="Blackstone").one()
        assert org.abn == "12 345 678 901" and org.status == "active"
    assert "11 digits" in c.post(f"/admin/customers/{org.id}", data={"abn": "123"}).text


def test_add_reviewer(op):
    c, S = op
    r = c.post("/admin/customers/2/users", data={"name": "Tara", "email": "tara@wtg.example",
                                                  "role": "customer_reviewer", "password": "temporary-pass-1"})
    assert "Tara added" in r.text and "Not on file" in r.text     # accreditation still to be entered by Tara
    assert "already in use" in c.post("/admin/customers/2/users", data={"name": "T", "email": "tara@wtg.example",
                                       "role": "customer_user", "password": "temporary-pass-1"}).text


# ---------- credits ----------
def test_grant_and_remove_credits_are_ledger_rows(op):
    c, S = op
    c.post("/admin/customers/2/credits", data={"action": "grant", "qty": 10, "reason": "Invoice INV-1 paid"})
    with S() as s:
        assert services.credit_balance(s, 2).available == 10
    assert "only 10 usable" in c.post("/admin/customers/2/credits", data={"action": "remove", "qty": 11, "reason": "x"}).text
    assert "reason is required" in c.post("/admin/customers/2/credits", data={"action": "grant", "qty": 1, "reason": " "}).text
    c.post("/admin/customers/2/credits", data={"action": "remove", "qty": 3, "reason": "Refund"})
    with S() as s:
        assert services.credit_balance(s, 2).available == 7
        rows = s.query(dbm.CreditLedger).filter_by(org_id=2).order_by(dbm.CreditLedger.id).all()
        assert [(r.type.value, r.qty) for r in rows] == [("purchase", 10), ("adjustment", -3)]
        assert rows[0].created_by == "Owner" and rows[1].reason == "Refund"
        assert s.query(dbm.AuditEvent).filter_by(action="credits_remove").count() == 1


# ---------- checks on a customer's behalf & queue ----------
def test_operator_runs_check_for_customer(op):
    c, S = op
    add_credits(S, org=2, qty=1)
    r = c.post("/admin/customers/2/upload", files={"file": ("SAMPLE-TMP-01.pdf", SAMPLE.read_bytes(), "application/pdf")},
               follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/checks/")
    cid = int(r.headers["location"].split("/")[-1])
    with S() as s:
        assert s.get(dbm.Check, cid).org_id == 2                  # belongs to the customer
        assert services.credit_balance(s, 2).available == 0      # customer's credit used
    assert c.get(f"/checks/{cid}").status_code == 200            # operator can open it
    q = c.get("/admin/queue").text
    assert "SAMPLE-TMP-01" in q and "Org B" in q


def test_queue_flags_overdue(op):
    c, S = op
    with S() as s:
        s.add(dbm.Check(org_id=2, doc_ref="OLD-TMP", filename="old.pdf", status=dbm.CheckStatus.uploaded,
                        created_at=datetime(2026, 1, 5, 9, 0, tzinfo=PERTH)))
        s.commit()
    q = c.get("/admin/queue").text
    assert "OLD-TMP" in q and "Overdue" in q


def test_operator_new_check_goes_to_customers(op):
    c, S = op
    r = c.get("/checks/new", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/admin/queue#run"
    r = c.post("/checks/upload", files={"file": ("x.pdf", SAMPLE.read_bytes(), "application/pdf")})
    assert r.status_code == 400 and "Work Queue" in r.json()["error"]
    for url, dest in (("/billing", "/admin/customers"), ("/checks", "/admin/queue")):
        r = c.get(url, follow_redirects=False)
        assert r.status_code == 303 and r.headers["location"] == dest


def test_operator_menu_and_dashboard(op):
    c, S = op
    page = c.get("/").text
    for text in ("Documents in process", "Recently completed", "Customers", "Org A", "Org B"):
        assert text in page
    nav = page.split("<nav>")[1].split("</nav>")[0]
    assert nav.index("Work Queue") < nav.index("Dashboard") < nav.index("Customers")
    assert "Credits &amp; Billing" not in nav and "New Check" not in nav and "My Checks" not in nav


def test_run_from_queue_uses_chosen_customers_credits(op):
    c, S = op
    add_credits(S, org=2, qty=2)
    q = c.get("/admin/queue").text
    assert "Org B — 2 credits" in q and "Org A — 0 credits (none left)" in q
    r = c.post("/admin/queue/run", data={"org_id": 2},
               files={"file": ("SAMPLE-TMP-01.pdf", SAMPLE.read_bytes(), "application/pdf")}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/checks/")
    with S() as s:
        assert services.credit_balance(s, 2).available == 1        # customer charged
        op_org = s.query(dbm.Organisation).filter_by(is_operator=True).one()
        assert s.query(dbm.CreditLedger).filter_by(org_id=op_org.id).count() == 0   # operator never holds credits
    r = c.post("/admin/queue/run", data={"org_id": 1},
               files={"file": ("SAMPLE-TMP-01.pdf", SAMPLE.read_bytes(), "application/pdf")})
    assert "Org A:" in r.text                                       # no credits -> refused with the customer named


def test_paused_customer_cannot_be_run(op):
    c, S = op
    add_credits(S, org=2, qty=1)
    with S() as s:
        s.get(dbm.Organisation, 2).status = "paused"; s.commit()
    r = c.post("/admin/queue/run", data={"org_id": 2},
               files={"file": ("SAMPLE-TMP-01.pdf", SAMPLE.read_bytes(), "application/pdf")})
    assert "is paused" in r.text


def test_operator_lands_on_work_queue(op):
    c, S = op
    c.cookies.clear()
    r = c.post("/login", data={"email": "op@x", "password": "correct-horse-battery", "next": "/"}, follow_redirects=False)
    assert r.headers["location"] == "/admin/queue"

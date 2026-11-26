"""Hosted pilot preview (A-53): invite sign-up, accreditation, historical/anonymised upload confirmation, AI cap."""
import pytest

from src.portal import db as dbm, preview, services
from tests.portal.test_workflow import env, upload, SAMPLE  # noqa: F401  (fixture)


@pytest.fixture
def prev(env, monkeypatch):
    monkeypatch.setenv("TMPCHECK_ENV", "preview")
    monkeypatch.setenv("TMPCHECK_INVITES", "GOOD123|Way to Go Traffic Management|5")
    return env


def form(**kw):
    base = dict(invite="GOOD123", name="Tara Test", email="tara@example.com", password="correct-horse-battery",
                level="AWTM", number="AWTM-KTS-24-8553-06", expiry="2030-06-30")
    base.update(kw); return base


def test_guard(monkeypatch):
    monkeypatch.setenv("TMPCHECK_ENV", "preview")
    for n in ("TMPCHECK_SECRET", "TMPCHECK_INVITES", "TMPCHECK_HTTPS"):
        monkeypatch.delenv(n, raising=False)
    with pytest.raises(RuntimeError, match="Preview needs"):
        preview.startup_guard()
    monkeypatch.setenv("TMPCHECK_ENV", "production")
    with pytest.raises(RuntimeError):
        preview.startup_guard()


def test_signup_creates_reviewer_with_credits_once(prev):
    c, S = prev
    c.cookies.clear()
    r = c.post("/signup", data=form(), follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/"
    with S() as s:
        u = s.query(dbm.User).filter_by(email="tara@example.com").one()
        assert u.role == "customer_reviewer" and u.accreditation_number == "AWTM-KTS-24-8553-06"
        assert services.credit_balance(s, u.org_id).available == 5
    c.cookies.clear()
    c.post("/signup", data=form(email="second@example.com"), follow_redirects=False)
    with S() as s:   # same org, credits not granted twice
        u2 = s.query(dbm.User).filter_by(email="second@example.com").one()
        assert services.credit_balance(s, u2.org_id).available == 5


@pytest.mark.parametrize("bad, msg", [({"invite": "NOPE"}, "not valid"), ({"number": ""}, "accreditation"),
                                      ({"password": "short"}, "10 characters"), ({"email": "a@x"}, "already exists")])
def test_signup_rejections(prev, bad, msg):
    c, _ = prev
    r = c.post("/signup", data=form(**bad), follow_redirects=False)
    assert r.status_code == 303 and msg.replace(" ", "%20") in r.headers["location"]


def test_signup_hidden_outside_preview(env):
    c, _ = env
    assert c.get("/signup").status_code == 404


def test_upload_needs_confirmation_in_preview(prev):
    c, S = prev
    from tests.portal.test_workflow import add_credits
    add_credits(S)
    r = upload(c)
    assert r.status_code == 400 and "historical or anonymised" in r.json()["error"]
    r = c.post("/checks/upload", data={"confirm_test_doc": "1"},
               files={"file": ("SAMPLE-TMP-01.pdf", SAMPLE.read_bytes(), "application/pdf")})
    assert r.status_code == 200


def test_ai_cap(prev, monkeypatch):
    _, S = prev
    with S() as s:
        s.add(dbm.Check(org_id=1, doc_ref="x", filename="x.pdf", status=dbm.CheckStatus.draft_review, ai_cost_usd="149.50"))
        s.commit()
        assert not preview.ai_cap_reached(s)[0]
        s.add(dbm.Check(org_id=1, doc_ref="y", filename="y.pdf", status=dbm.CheckStatus.draft_review, ai_cost_usd="1.00"))
        s.commit()
        capped, why = preview.ai_cap_reached(s)
        assert capped and "cap reached" in why

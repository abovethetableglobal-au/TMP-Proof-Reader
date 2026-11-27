"""P-G3 (Owner 2026-11-27): reviewer accreditation captured in the portal and required before review."""
from datetime import date, timedelta

from src.portal import auth, db as dbm
from tests.portal.test_workflow import add_credits, env, upload  # noqa: F401  (env is a fixture)


def _set_accreditation(S, email, level=None, number=None, expiry=None):
    with S() as s:
        u = s.query(dbm.User).filter_by(email=email).one()
        u.accreditation_level, u.accreditation_number, u.accreditation_expiry = level, number, expiry
        s.commit()


def _draft(c, S):
    add_credits(S, qty=1)
    cid = upload(c).json()["id"]
    with S() as s:
        fid = s.query(dbm.Finding).filter_by(check_id=cid).first().id
    return cid, fid


def test_reviewer_without_accreditation_cannot_decide(env):
    c, S = env
    cid, fid = _draft(c, S)
    _set_accreditation(S, "a@x")                       # nothing on file
    r = c.post(f"/checks/{cid}/findings/{fid}", data={"decision": "accepted", "note": ""})
    assert r.status_code == 403 and "Account page" in r.text
    with S() as s:
        assert s.get(dbm.Finding, fid).disposition == "pending"


def test_expired_accreditation_blocks_final(env):
    c, S = env
    cid, _ = _draft(c, S)
    _set_accreditation(S, "a@x", "AWTM", "A-1", date.today() - timedelta(days=1))
    assert c.post(f"/checks/{cid}/final").status_code == 403


def test_save_accreditation_and_validation(env):
    c, S = env
    _set_accreditation(S, "a@x")
    page = c.get("/account").text
    assert "You need current accreditation on file" in page
    future = (date.today() + timedelta(days=400)).isoformat()
    bad = [({"level": "XYZ", "number": "1", "expiry": future}, "accreditation level"),
           ({"level": "RTM", "number": " ", "expiry": future}, "certificate number"),
           ({"level": "RTM", "number": "R-9", "expiry": "not-a-date"}, "expiry date"),
           ({"level": "RTM", "number": "R-9", "expiry": "2020-01-01"}, "expired")]
    for data, msg in bad:
        r = c.post("/account/accreditation", data=data)
        assert msg in r.text
    r = c.post("/account/accreditation", data={"level": "RTM", "number": "R-9", "expiry": future})
    assert "Accreditation saved" in r.text and "RTM R-9" in r.text
    with S() as s:
        u = s.query(dbm.User).filter_by(email="a@x").one()
        assert auth.accreditation_current(u)
        assert s.query(dbm.AuditEvent).filter_by(action="accreditation_saved").count() == 1


def test_final_report_names_reviewer_accreditation(env):
    c, S = env
    cid, _ = _draft(c, S)
    with S() as s:
        ids = [f.id for f in s.query(dbm.Finding).filter_by(check_id=cid)]
    for fid in ids:
        c.post(f"/checks/{cid}/findings/{fid}", data={"decision": "accepted", "note": ""})
    c.post(f"/checks/{cid}/final")
    with S() as s:
        chk = s.get(dbm.Check, cid)
        assert chk.status == dbm.CheckStatus.final_issued
        assert chk.reviewer_name == "Alice (AWTM A-1234, valid to 01/01/2099)"


def test_non_reviewer_has_no_accreditation_form(env):
    c, S = env
    from tests.portal.conftest import login
    login(c, "u@x")
    page = c.get("/account").text
    assert "My Account" in page and "Save accreditation" not in page

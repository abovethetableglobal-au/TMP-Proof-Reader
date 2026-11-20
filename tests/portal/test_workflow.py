"""Functional tests: upload → check → draft → reviewer decisions → final, with credit rules."""
import os
from datetime import timedelta
from pathlib import Path

import pytest

os.environ["TMPCHECK_ENV"] = "local"
os.environ.setdefault("TMPCHECK_DB_URL", "sqlite://")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.portal import app as appmod, db as dbm, processing, services

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "test-library" / "samples" / "SAMPLE-TMP-01.pdf"


@pytest.fixture
def env(tmp_path, monkeypatch):
    if not SAMPLE.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("m", SAMPLE.with_name("make_sample_tmp.py"))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.main()
    eng = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    dbm.Base.metadata.create_all(eng)
    S = sessionmaker(bind=eng, expire_on_commit=False)
    monkeypatch.setattr(processing, "session_factory", S)
    monkeypatch.setattr(processing, "STORAGE", tmp_path)
    monkeypatch.delenv("TMPCHECK_AI_PASSES", raising=False)
    s = S()
    a = dbm.Organisation(name="Org A"); b = dbm.Organisation(name="Org B")
    s.add_all([a, b]); s.flush()
    s.add_all([dbm.User(org_id=a.id, name="Alice", email="a@x"), dbm.User(org_id=b.id, name="Bob", email="b@x")])
    s.commit()

    def get_db():
        d = S()
        try:
            yield d
        finally:
            d.close()
    appmod.app.dependency_overrides[appmod.get_db] = get_db
    os.environ["TMPCHECK_DEV_USER"] = "1"
    with TestClient(appmod.app) as c:
        yield c, S
    appmod.app.dependency_overrides.clear()


def add_credits(S, org=1, qty=2):
    with S() as s:
        r = dbm.CreditLedger(org_id=org, type=dbm.LedgerType.purchase, qty=qty,
                             expires_at=dbm.utcnow() + timedelta(days=365), created_by="test")
        s.add(r); s.flush(); r.lot_id = r.id; s.commit()


def balance(S, org=1):
    with S() as s:
        return services.credit_balance(s, org).available


def upload(c, name="SAMPLE-TMP-01.pdf", data=None):
    return c.post("/checks/upload", files={"file": (name, data if data is not None else SAMPLE.read_bytes(),
                                                    "application/pdf")})


def test_full_workflow(env):
    c, S = env
    add_credits(S, qty=2)
    r = upload(c)
    assert r.status_code == 200
    cid = r.json()["id"]
    page = c.get(f"/checks/{cid}").text
    assert "Draft — awaiting reviewer" in page
    assert balance(S) == 1                                    # A-24: consumed at draft delivery
    with S() as s:
        fs = s.query(dbm.Finding).filter_by(check_id=cid).all()
        assert {f.rule for f in fs} >= {"PH-ANGLE", "PH-X", "PH-TBA", "JX-QLD", "PG-HEADER", "DUP-SENT", "PH-DATE"}
        ids = [f.id for f in fs]
        chk = s.get(dbm.Check, cid)
        original = Path(chk.storage_path)
    assert original.read_bytes() == SAMPLE.read_bytes()        # original never modified

    # final blocked while findings pending
    assert "still need a decision" in c.post(f"/checks/{cid}/final").text
    with S() as s:
        assert s.get(dbm.Check, cid).status == dbm.CheckStatus.draft_review

    # edit without note is refused
    c.post(f"/checks/{cid}/findings/{ids[0]}", data={"decision": "edited", "note": ""})
    with S() as s:
        assert s.get(dbm.Finding, ids[0]).disposition == "pending"

    for i, fid in enumerate(ids):
        c.post(f"/checks/{cid}/findings/{fid}", data={"decision": "rejected" if i == 0 else "accepted", "note": ""})
    c.post(f"/checks/{cid}/final")
    with S() as s:
        assert s.get(dbm.Check, cid).status == dbm.CheckStatus.final_issued
    dash = c.get("/").text
    assert "Final issued" in dash
    hist = c.get("/billing").text
    assert "Credit used" in hist and "SAMPLE-TMP-01" in hist


def test_no_credits_rejected(env):
    c, S = env
    r = upload(c)
    assert r.status_code == 400 and "no credits" in r.json()["error"].lower()
    with S() as s:
        assert s.query(dbm.Check).count() == 0


@pytest.mark.parametrize("name,data,msg", [
    ("plan.doc", b"\xd0\xcf\x11\xe0", "not supported"),
    ("plan.pdf", b"", "empty"),
    ("plan.pdf", b"PK\x03\x04renamed zip", "not appear to be a valid PDF"),
])
def test_invalid_files_rejected(env, name, data, msg):
    c, S = env
    add_credits(S)
    r = upload(c, name, data)
    assert r.status_code == 400 and msg in r.json()["error"]
    assert balance(S) == 2


def test_oversize_rejected(env):
    c, S = env
    add_credits(S)
    r = upload(c, "big.pdf", b"%PDF-" + b"0" * (20 * 1048576))
    assert r.status_code == 400 and "maximum size" in r.json()["error"]


def test_corrupt_pdf_fails_without_credit(env):
    c, S = env
    add_credits(S)
    r = upload(c, "broken.pdf", b"%PDF-1.7 this is not really a pdf")
    cid = r.json()["id"]
    page = c.get(f"/checks/{cid}").text
    assert "could not be completed" in page and "No credit was used" in page
    assert balance(S) == 2


def test_other_org_cannot_see_check(env):
    c, S = env
    add_credits(S)
    cid = upload(c).json()["id"]
    os.environ["TMPCHECK_DEV_USER"] = "2"
    try:
        assert c.get(f"/checks/{cid}").status_code == 404
        assert c.get(f"/checks/{cid}/original").status_code == 404
        assert c.post(f"/checks/{cid}/final").status_code == 404
        assert "SAMPLE-TMP-01" not in c.get("/checks").text
    finally:
        os.environ["TMPCHECK_DEV_USER"] = "1"


def test_page_limit_a26(env, monkeypatch):
    c, S = env
    add_credits(S)
    from src.portal import config
    cfg = dict(config.settings()); cfg["upload"] = {**cfg["upload"], "max_total_pages": 5}
    monkeypatch.setattr(processing, "settings", lambda: cfg)
    cid = upload(c).json()["id"]            # sample has 6 pages
    page = c.get(f"/checks/{cid}").text
    assert "has 6 pages. The limit is 5 pages including drawings" in page
    assert balance(S) == 2


def test_dedupe_merges_same_issue_keeps_distinct():
    ev = "<Detail consultation/communication with relevant agencies as required, e.g. PTA, emergency services, LGAs>"
    items = [("deterministic", {"page": 25, "severity": "Moderate", "evidence": ev[:60], "issue": "Template instruction left", "rule": "PH-ANGLE"}),
             ("ai", {"page": 25, "severity": "Major", "evidence": ev, "issue": "Template instruction is left in and no consultation is described.", "pass": "C"}),
             ("ai", {"page": 25, "severity": "Major", "evidence": ev[:80], "issue": "Placeholder not replaced.", "pass": "A"}),
             ("ai", {"page": 26, "severity": "Major", "evidence": ev, "issue": "Same text, other page", "pass": "C"}),
             ("ai", {"page": 25, "severity": "Minor", "evidence": "Speed limit 60km/h should read 60 km/h", "issue": "Unit spacing", "pass": "A"})]
    out = processing.dedupe(items)
    assert len(out) == 3
    src, merged = out[0]
    assert merged["severity"] == "Major" and merged["rule"] == "PH-ANGLE" and merged["evidence"] == ev
    assert src == "AI A, AI C, rules"


def test_export_json(env):
    c, S = env
    add_credits(S)
    cid = upload(c).json()["id"]
    r = c.get(f"/checks/{cid}/findings.json")
    assert r.status_code == 200 and len(r.json()["findings"]) == 7


def test_grouped_finding_renders_pages_and_list(env):
    c, S = env
    add_credits(S)
    cid = upload(c).json()["id"]
    with S() as s:
        s.add(dbm.Finding(check_id=cid, severity="Minor", page=9, section="", pages="9, 21",
                          evidence="• p9: Unit spacing\n• p21: Volume spacing", issue="Style inconsistencies (2 items)",
                          source="AI A"))
        s.commit()
    html = c.get(f"/checks/{cid}").text
    assert "Pages 9, 21" in html and 'class="list"' in html
    assert c.get(f"/checks/{cid}/findings.json").json()["findings"][-1]["pages"] == "9, 21"

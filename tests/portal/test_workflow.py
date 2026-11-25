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
from tests.portal.conftest import login

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
    from tests.portal.conftest import PW_HASH
    s.add_all([dbm.User(org_id=a.id, name="Alice", email="a@x", role="customer_reviewer", password_hash=PW_HASH),
               dbm.User(org_id=b.id, name="Bob", email="b@x", password_hash=PW_HASH),
               dbm.User(org_id=a.id, name="Uma", email="u@x", role="customer_user", password_hash=PW_HASH)])
    s.commit()

    def get_db():
        d = S()
        try:
            yield d
        finally:
            d.close()
    appmod.app.dependency_overrides[appmod.get_db] = get_db
    with TestClient(appmod.app) as c:
        login(c, "a@x")
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
    login(c, "b@x")
    assert c.get(f"/checks/{cid}").status_code == 404
    assert c.get(f"/checks/{cid}/original").status_code == 404
    assert c.get(f"/checks/{cid}/report.pdf").status_code == 404
    assert c.post(f"/checks/{cid}/final").status_code in (403, 404)
    assert "SAMPLE-TMP-01" not in c.get("/checks").text
    with S() as s:
        assert s.query(dbm.AuditEvent).filter_by(action="denied_other_org").count() >= 3


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


def test_two_ai_runs_combined_and_grouped(env, monkeypatch):
    """BENCH-04: AI passes run twice; findings from both runs are grouped; costs add up."""
    c, S = env
    add_credits(S)
    from src.tmpcheck import llm_checks, consolidate as cons
    calls = {"n": 0}

    def fake_run(pdf, passes, dry_run=False):
        calls["n"] += 1
        f = {"page": 4, "section": "3", "evidence": "Signage will be installed in accordance with TMR requirements.",
             "issue": f"Queensland TMR referenced (run {calls['n']})", "fix": "Use WA terms", "severity": "Moderate",
             "related_pages": [], "pass": "C"}
        return {"passes": {"C": {"findings": [f]}}, "usd_total": 1.25}
    monkeypatch.setattr(llm_checks, "run", fake_run)
    # grouping call returns every finding on its own (the page-level merge already combined the overlaps)
    monkeypatch.setattr(cons, "group_findings", lambda fs: ([([i], "issue") for i in range(len(fs))], 0.10))
    monkeypatch.setenv("TMPCHECK_AI_PASSES", "C")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-dummy")
    monkeypatch.delenv("TMPCHECK_AI_RUNS", raising=False)
    cid = upload(c).json()["id"]
    assert calls["n"] == 2
    with S() as s:
        chk = s.get(dbm.Check, cid)
        assert chk.ai_passes == "C ×2" and chk.ai_cost_usd == "2.60"
        tmr = [f for f in s.query(dbm.Finding).filter_by(check_id=cid).all() if f.page == 4 and "TMR" in (f.issue + f.evidence)]
        # both AI copies and the rule finding overlap on the same evidence → merged into one finding
        assert len(tmr) == 1 and "rules" in tmr[0].source and "AI C" in tmr[0].source


def test_ai_runs_setting(monkeypatch):
    monkeypatch.setenv("TMPCHECK_AI_RUNS", "1")
    assert processing.ai_runs() == 1
    monkeypatch.setenv("TMPCHECK_AI_RUNS", "9")
    assert processing.ai_runs() == 3
    monkeypatch.delenv("TMPCHECK_AI_RUNS")
    assert processing.ai_runs() == 2          # config default (BENCH-04)


def test_word_form_rules():
    from src.tmpcheck.det_checks import WORD_FORM
    hits = lambda t: [r for r, rx, _ in WORD_FORM if rx.search(t)]
    assert hits("volume is upto 500 vph") == ["WF-JOINED"]
    assert hits("at least 2 week s notice") == ["WF-SPLIT"]
    assert hits("Cert No.KTS-24") == ["WF-NOSPACE"]
    assert hits("No. 5, setup, up to 500") == []


def test_report_and_annotated_outputs(env):
    """D-11/D-12: draft outputs watermarked; final stored at issue; rejected findings excluded; original intact."""
    import pymupdf
    c, S = env
    add_credits(S)
    cid = upload(c).json()["id"]
    r = c.get(f"/checks/{cid}/report.pdf")
    assert r.status_code == 200 and r.content[:5] == b"%PDF-" and "DRAFT" in r.headers["content-disposition"]
    rep = pymupdf.open(stream=r.content, filetype="pdf")
    text = "".join(p.get_text() for p in rep)
    assert "TMP Check Report" in text and "DRAFT" in text and "F-007" in text
    for bad in ("compliant", "Compliant", "100%", " safe ", "approved"):
        assert bad not in text, bad
    a = c.get(f"/checks/{cid}/annotated.pdf")
    ann = pymupdf.open(stream=a.content, filetype="pdf")
    orig = pymupdf.open(SAMPLE)
    assert ann.page_count == orig.page_count                                  # pagination preserved
    assert all(x.get_text("text", flags=0) in y.get_text() or y.get_text().startswith(x.get_text())
               for x, y in zip(orig, ann))                                    # original content unchanged
    assert sum(len(list(p.annots())) for p in ann) >= 7

    with S() as s:
        fs = s.query(dbm.Finding).filter_by(check_id=cid).order_by(dbm.Finding.id).all()
        for i, f in enumerate(fs):
            f.disposition = "rejected" if f.rule == "PH-X" else "accepted"
        s.commit()
    c.post(f"/checks/{cid}/final")
    with S() as s:
        chk = s.get(dbm.Check, cid)
        assert chk.status == dbm.CheckStatus.final_issued and chk.reviewer_name == "Alice"
    fin = pymupdf.open(stream=c.get(f"/checks/{cid}/report.pdf").content, filetype="pdf")
    ftext = "".join(p.get_text() for p in fin)
    assert "FINAL" in ftext and "DRAFT" not in ftext and "Alice" in ftext
    flat = " ".join(ftext.split())
    assert "XXXX" not in flat and "1 was rejected" in flat                    # rejected finding left out
    assert c.get(f"/checks/{cid}/annotated.pdf").status_code == 200


def test_sign_in_required_and_csrf_and_roles(env):
    c, S = env
    add_credits(S)
    cid = upload(c).json()["id"]
    with S() as s:
        fid = s.query(dbm.Finding).filter_by(check_id=cid).first().id
    # signed out: pages redirect to sign-in, actions refused
    c.cookies.clear()
    r = c.get("/", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/login")
    assert c.post("/checks/upload", files={"file": ("a.pdf", b"%PDF-1", "application/pdf")}).status_code == 401
    # wrong password
    assert "not recognised" in c.get(login(c, "a@x", "wrong-password-x").headers["location"],).text
    # CSRF: signed in but no token → 403
    login(c, "a@x")
    hdr = c.headers.pop("X-CSRF-Token")
    assert c.post(f"/checks/{cid}/findings/{fid}", data={"decision": "accepted"}).status_code == 403
    c.headers["X-CSRF-Token"] = hdr
    # customer_user: can view and upload, cannot decide or issue final
    login(c, "u@x")
    page = c.get(f"/checks/{cid}").text
    assert "Only your organisation's accredited reviewer" in page and 'value="accepted"' not in page
    assert c.post(f"/checks/{cid}/findings/{fid}", data={"decision": "accepted"}).status_code == 403
    assert c.post(f"/checks/{cid}/final").status_code == 403
    # reviewer can decide
    login(c, "a@x")
    assert c.post(f"/checks/{cid}/findings/{fid}", data={"decision": "accepted"}).status_code == 200
    with S() as s:
        actions = {e.action for e in s.query(dbm.AuditEvent).all()}
    assert {"login", "login_failed", "upload", "view_check", "finding_decision"} <= actions


def test_logout_ends_session(env):
    c, S = env
    tok = c.cookies.get("tmpcheck_session")
    assert c.post("/logout", follow_redirects=False).status_code == 303
    c.cookies.set("tmpcheck_session", tok)
    assert c.get("/", follow_redirects=False).status_code == 303          # old token no longer valid


def test_password_rules():
    from src.portal import auth
    import pytest as _p
    with _p.raises(ValueError):
        auth.hash_password("short")
    h = auth.hash_password("a-long-enough-password")
    assert auth.verify_password("a-long-enough-password", h) and not auth.verify_password("nope-nope-nope", h)


def test_interrupted_check_marked_failed_at_startup(env):
    c, S = env
    add_credits(S)
    with S() as s:
        s.add(dbm.Check(org_id=1, doc_ref="STUCK", filename="stuck.pdf", status=dbm.CheckStatus.processing))
        s.commit()
    assert processing.recover_interrupted() == 1
    with S() as s:
        chk = s.query(dbm.Check).filter_by(doc_ref="STUCK").one()
        assert chk.status == dbm.CheckStatus.failed and "interrupted" in chk.failure_reason
    assert balance(S) == 2


def test_processing_time_recorded(env):
    c, S = env
    add_credits(S)
    r = upload(c, "broken.pdf", b"%PDF-1.7 this is not really a pdf")
    cid = r.json()["id"]
    with S() as s:
        chk = s.get(dbm.Check, cid)
        assert chk.processing_started_at and chk.processing_finished_at and chk.processing_seconds is not None
        assert "Failed" in chk.timings
    assert "Processing time:" in c.get(f"/checks/{cid}").text
    assert c.get(f"/checks/{cid}/findings.json").json()["processing_seconds"] is not None

"""Report downloads (Owner 2026-11-27): download by default, view on request, both files as a ZIP."""
import io
import zipfile

from src.portal import db as dbm
from tests.portal.test_workflow import add_credits, env, upload  # noqa: F401  (env is a fixture)


def _draft(c, S):
    add_credits(S, qty=1)
    return upload(c).json()["id"]


def test_pdfs_download_by_default_and_view_on_request(env):
    c, S = env
    cid = _draft(c, S)
    for path in ("report.pdf", "annotated.pdf"):
        r = c.get(f"/checks/{cid}/{path}")
        assert r.status_code == 200 and r.content.startswith(b"%PDF")
        assert r.headers["content-disposition"].startswith("attachment;") and "(DRAFT).pdf" in r.headers["content-disposition"]
        v = c.get(f"/checks/{cid}/{path}?view=1")
        assert v.headers["content-disposition"].startswith("inline;")


def test_zip_contains_report_and_annotated(env):
    c, S = env
    cid = _draft(c, S)
    r = c.get(f"/checks/{cid}/download.zip")
    assert r.status_code == 200 and r.headers["content-type"] == "application/zip"
    names = zipfile.ZipFile(io.BytesIO(r.content)).namelist()
    assert sorted(names) == ["SAMPLE-TMP-01 - TMP Check annotated (DRAFT).pdf", "SAMPLE-TMP-01 - TMP Check report (DRAFT).pdf"]


def test_final_zip_uses_stored_final_files(env):
    c, S = env
    cid = _draft(c, S)
    with S() as s:
        for f in s.query(dbm.Finding).filter_by(check_id=cid):
            f.disposition = "accepted"
        s.commit()
    c.post(f"/checks/{cid}/final")
    names = zipfile.ZipFile(io.BytesIO(c.get(f"/checks/{cid}/download.zip").content)).namelist()
    assert all("(final)" in n for n in names) and len(names) == 2


def test_download_buttons_shown(env):
    c, S = env
    cid = _draft(c, S)
    page = c.get(f"/checks/{cid}").text
    assert "Download report" in page and "Download both (ZIP)" in page and "?view=1" in page
    assert f"/checks/{cid}/download.zip" in c.get("/checks").text


def test_other_org_cannot_download(env):
    c, S = env
    cid = _draft(c, S)
    from tests.portal.conftest import login
    login(c, "b@x")
    assert c.get(f"/checks/{cid}/download.zip").status_code == 404

"""Word TMPs: findings as Word comments on a copy of the original .docx (Owner 2026-11-27)."""
import io
import shutil
import zipfile

import pytest
from docx import Document

from src.portal import db as dbm
from tests.portal.test_workflow import add_credits, env  # noqa: F401  (env is a fixture)

pytestmark = pytest.mark.skipif(not (shutil.which("soffice") or shutil.which("libreoffice")),
                                reason="LibreOffice needed to convert Word uploads")


def _make_docx() -> bytes:
    d = Document()
    d.add_heading("Traffic Management Plan", 1)
    d.add_paragraph("Prepared by XXXXX (AWTM Cert No. XXXX) following a site inspection.")
    d.add_paragraph("Sub-contractor: TBA")
    d.add_paragraph("<Detail consultation with relevant agencies as required, e.g. PTA, emergency services>")
    t = d.add_table(rows=1, cols=2)
    t.cell(0, 0).text = "Incident reported to"
    t.cell(0, 1).text = "Supervisor / TMR / Other"
    buf = io.BytesIO(); d.save(buf)
    return buf.getvalue()


def _texts(doc) -> list[str]:
    from src.tmpcheck.outputs import _docx_paragraphs
    return [p.text for p in _docx_paragraphs(doc)]


def test_word_upload_gets_commented_copy(env):
    c, S = env
    add_credits(S, qty=1)
    src = _make_docx()
    r = c.post("/checks/upload", files={"file": ("WORD-TMP-01.docx", src,
               "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
    assert r.status_code == 200, r.text
    cid = r.json()["id"]
    page = c.get(f"/checks/{cid}").text
    assert "Download Word with comments" in page

    resp = c.get(f"/checks/{cid}/comments.docx")
    assert resp.status_code == 200 and "attachment;" in resp.headers["content-disposition"]
    out = Document(io.BytesIO(resp.content))
    comments = list(out.comments)
    with S() as s:
        n_findings = s.query(dbm.Finding).filter_by(check_id=cid).count()
    assert n_findings > 0
    assert len(comments) >= 2                                  # findings + the header comment
    joined = "\n".join(cm.text for cm in comments)
    assert "TMP Check" in joined and "F-0" in joined
    assert _texts(out) == _texts(Document(io.BytesIO(src)))   # document text unchanged — comments only

    names = zipfile.ZipFile(io.BytesIO(c.get(f"/checks/{cid}/download.zip").content)).namelist()
    assert "WORD-TMP-01 - TMP Check Word comments (DRAFT).docx" in names
    assert "WORD-TMP-01 - source TMP.docx" in names


def test_pdf_upload_has_no_word_option(env):
    c, S = env
    from tests.portal.test_workflow import upload
    add_credits(S, qty=1)
    cid = upload(c).json()["id"]
    assert "Download Word with comments" not in c.get(f"/checks/{cid}").text
    assert c.get(f"/checks/{cid}/comments.docx").status_code == 404

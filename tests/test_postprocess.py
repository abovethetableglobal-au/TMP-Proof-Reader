"""Regression tests for draft-report review defects D1-D5 (synthetic PDF, no customer data)."""
import pymupdf
import pytest

from src.tmpcheck import det_checks
from src.tmpcheck.postprocess import locate, merge, validate

NOTE = "Note 3: Cones shall be placed at 4 m spacing through the taper and 8 m along the work area at all times."


@pytest.fixture
def pdf(tmp_path):
    doc = pymupdf.open()
    body = doc.new_page()  # portrait body page
    body.insert_text((50, 80), "Works hours are 7:00am to 5:00pm Monday to Friday.")
    body.insert_text((50, 100), "The speed limit is 60km/h on")
    body.insert_text((300, 400), "Kanimbla Road east of the site.")
    for n in (1, 2):  # portrait TGS sheets with identical standard notes (D5)
        p = doc.new_page()
        p.insert_text((50, 60), f"TGS {n:02d}  Traffic Guidance Scheme")
        p.insert_text((50, 80), "Drawing No : 01   Drawn by : AB   Not to scale")
        p.insert_text((50, 120), NOTE, fontsize=7)
    path = tmp_path / "synthetic.pdf"
    doc.save(path)
    return path


def F(**k):
    base = dict(page=1, section="1", evidence="", issue="x", fix="", severity="Minor", related_pages=[])
    return {**base, **k}


def test_d1_locator_and_validator_agree(pdf):
    doc = pymupdf.open(pdf)
    ok = F(evidence="7:00am to 5:00pm Monday")
    split = F(evidence="60km/h on Kanimbla Road", severity="Major")   # text spans separate blocks
    bad = F(evidence="Works hours are 6:00am", severity="Major")
    validate([ok, split, bad], doc)
    assert ok["evidence_check"] == "verified" and ok["bbox"] and ok["outcome"] == "Potential issue"
    assert bad["severity"] == "Query" and bad["original_severity"] == "Major"
    assert bad["outcome"] == "Unable to verify"
    # whatever the validator says, the annotation locator must agree
    for f in (ok, split, bad):
        assert (f["evidence_check"] == "verified") == bool(locate(doc[f["page"] - 1], f["evidence"]))


def test_d2_visual_only_critical_held(pdf):
    doc = pymupdf.open(pdf)
    crit = F(page=2, evidence="VISUAL: no advance warning sign shown", severity="Critical")
    minor = F(page=2, evidence="VISUAL: label clipped", severity="Minor")
    validate([crit, minor], doc)
    assert crit["severity"] == "Query" and crit["original_severity"] == "Critical"
    assert crit["outcome"] == "Unable to verify"
    assert minor["severity"] == "Minor"


def test_d3_query_never_labelled_potential_issue():
    out = merge([F(severity="Query", outcome="Potential issue"), F(page=9, issue="other", severity="Minor")])
    assert {f["severity"]: f["outcome"] for f in out} == {"Query": "Unable to verify", "Minor": "Potential issue"}


def test_d4_duplicates_merged():
    a = F(page=2, issue="Note 3 cone spacing conflicts with the TMP text (4 m vs 9 m)", severity="Moderate", id="B-004", **{"pass": "B"})
    b = F(page=3, issue="Note 3 cone spacing conflicts with the TMP text (4 m vs 9 m).", severity="Major", id="D-002", **{"pass": "D"})
    c = F(page=5, evidence="Appendix E", issue="Appendix E is empty", id="C-010", **{"pass": "C"})
    d = F(page=5, evidence="Appendix E", issue="Appendix E contains no content", related_pages=[1], id="B-011", **{"pass": "B"})
    e = F(page=7, issue="Spelling: 'recieve'")
    out = merge([a, b, c, d, e])
    assert len(out) == 3
    cone = next(f for f in out if "cone" in f["issue"])
    assert cone["severity"] == "Major" and set(cone["related_pages"]) == {2} and cone["merged_from"][0]["id"] == "B-004"


def test_d4_distinct_rule_findings_not_merged():
    x = dict(rule="PH-X", page=3, evidence="XX", issue="Placeholder 'XX…' not completed", severity="Moderate")
    y = dict(rule="PH-X", page=8, evidence="XX", issue="Placeholder 'XX…' not completed", severity="Moderate")
    assert len(merge([x, y])) == 2


def test_d5_dup_sent_ignores_repeated_tgs_notes(pdf):
    res = det_checks.run(pdf)
    assert "DUP-SENT" not in res["by_rule"]
    assert all(f["outcome"] == ("Unable to verify" if f["severity"] == "Query" else "Potential issue") for f in res["findings"])


def test_def_l06_1_style_variants_verified_across_pages(tmp_path):
    doc = pymupdf.open()
    doc.new_page().insert_text((50, 80), "Access is via the car park on Hay Street.")
    doc.new_page().insert_text((50, 80), "The carpark entry will remain open.")
    path = tmp_path / "v.pdf"
    doc.save(path)
    doc = pymupdf.open(path)
    ok = F(evidence="car park / carpark", severity="Minor")
    bad = F(evidence="car park / car-park bay", severity="Minor")
    validate([ok, bad], doc)
    assert ok["evidence_check"] == "verified" and ok["severity"] == "Minor"
    assert ok["variant_pages"] == {"car park": 1, "carpark": 2}
    assert bad["severity"] == "Query"

"""Fixes from the check 14/15 output review (2026-11-25)."""
import pymupdf

from src.portal import processing
from src.tmpcheck import det_checks, outputs
from src.tmpcheck.postprocess import locate


def _page(text):
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=10)
    return doc, page


def test_tokens_fold_ligatures():
    from src.tmpcheck.postprocess import _tok
    assert _tok("tra\ufb03c") == _tok("traffic") == ["traffic"]   # 'ﬃ' ligature as extracted from PDFs


def test_highlight_uses_word_locator_across_lines():
    doc, page = _page("the quote starts here and\ncontinues on the next line")
    assert outputs._locate(page, "starts here and continues on the next")


def test_merge_keeps_located_evidence_and_severity():
    located = {"page": 5, "severity": "Minor", "evidence": "short quote on page", "evidence_check": "verified", "issue": "a"}
    unlocated = {"page": 5, "severity": "Major", "evidence": "a much longer quote that is not on the page at all",
                 "evidence_check": "NOT FOUND on cited page", "issue": "a longer issue text"}
    src, m = processing.merge([("ai", located), ("ai", unlocated)])
    assert m["evidence"] == "short quote on page" and m["severity"] == "Minor" and m["outcome"] == "Potential issue"


def test_merge_without_located_quote_is_query():
    a = {"page": 5, "severity": "Major", "evidence": "x" * 30, "evidence_check": "NOT FOUND on cited page", "issue": "a"}
    b = dict(a, severity="Moderate")
    _, m = processing.merge([("ai", a), ("ai", b)])
    assert m["severity"] == "Query" and m["outcome"] == "Unable to verify"


def test_merge_visual_only_critical_held_as_query():
    a = {"page": 59, "severity": "Critical", "evidence": "VISUAL: truck in lane", "evidence_check": "visual — reviewer to confirm", "issue": "a"}
    b = dict(a, severity="Major")
    _, m = processing.merge([("ai", a), ("ai", b)])
    assert m["severity"] == "Query"


def test_snippet_and_page_wording():
    s = det_checks.snippet("word " * 40)
    assert s.endswith("…") and not s[:-1].endswith(" ") and len(s) <= det_checks.MAX_EV + 1
    assert det_checks.page_list([38]) == "page 38"
    assert det_checks.page_list([35, 36]) == "pages 35 and 36"


def test_every_rule_has_an_action():
    rules = [r for r, *_ in det_checks.PLACEHOLDERS + det_checks.INTERSTATE + det_checks.JURISDICTION + det_checks.WORD_FORM]
    assert all(det_checks.ACTIONS.get(r) for r in rules + ["PG-HEADER", "DUP-SENT"])


def test_report_states_category_e_result():
    meta = outputs.Meta(doc_ref="T", filename="t.pdf", organisation="O", pages=1, uploaded=None, final=False)
    html = outputs.report_html(meta, [], [])
    assert "No category E rule was triggered" in html

"""Template-diff completeness check (category C) — rule WA-COP-4.2.1-001.

WA Code §4.2.1 (March 2026) requires TMPs to be based on a Main Roads TMP template with
all section headings retained (non-applicable sections marked 'not applicable').
This module compares a submitted TMP (PDF) against the heading list of the blank template (DOCX).

Usage:
    python -m src.tmpcheck.template_diff <template.docx> <submission.pdf> [out.json]
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf
from docx import Document

RULE = {
    "rule_id": "WA-COP-4.2.1-001",
    "source": "Main Roads WA Traffic Management for Works on Roads Code of Practice",
    "edition": "March 2026",
    "clause": "§4.2.1 (p26)",
}
MATCH_THRESHOLD = 0.88
NUM_PREFIX = re.compile(r"^\s*(\d+(\.\d+)*\.?)\s+")
LEADER = re.compile(r"\.{4,}|…{2,}")  # table-of-contents dot leaders


def norm(s: str) -> str:
    s = NUM_PREFIX.sub("", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def template_headings(docx_path: Path) -> list[dict]:
    out = []
    for p in Document(docx_path).paragraphs:
        st = p.style.name
        if st.lower().startswith("heading") and p.text.strip():
            out.append({"level": int(st.split()[-1]), "text": p.text.strip(), "key": norm(p.text)})
    return out


def submission_lines(pdf_path: Path) -> list[dict]:
    """Candidate heading lines from the body (TOC lines with dot leaders excluded)."""
    lines = []
    doc = pymupdf.open(pdf_path)
    for pno, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = "".join(s["text"] for s in line["spans"]).strip()
                if not text or LEADER.search(text) or len(text) > 120:
                    continue
                lines.append({"page": pno, "text": text, "key": norm(text),
                              "bbox": [round(v, 1) for v in line["bbox"]]})
    return lines


def diff(template_docx: Path, submission_pdf: Path) -> dict:
    heads = template_headings(template_docx)
    lines = submission_lines(submission_pdf)
    by_key = {}
    for ln in lines:
        by_key.setdefault(ln["key"], ln)
    findings, matched = [], 0
    cursor_page = 1
    for h in heads:
        hit = by_key.get(h["key"])
        if hit is None:  # tolerate minor wording variation
            best = max(lines, key=lambda ln: SequenceMatcher(None, h["key"], ln["key"]).ratio(), default=None)
            if best and SequenceMatcher(None, h["key"], best["key"]).ratio() >= MATCH_THRESHOLD:
                hit = best
        if hit:
            matched += 1
            cursor_page = hit["page"]
            continue
        findings.append({
            "category": "C Completeness",
            "severity": "Major",
            "outcome": "Potential issue",
            "page": cursor_page,  # where the heading would be expected (after previous matched heading)
            "evidence": f"Template heading not found: '{h['text']}' (level {h['level']})",
            "issue": "Required template section heading missing. The Code requires all template headings to be "
                     "retained, with non-applicable sections marked 'not applicable'.",
            "action": f"Reinstate heading '{h['text']}' and complete it or mark it 'not applicable'.",
            **RULE,
        })
    return {"template_headings": len(heads), "matched": matched, "missing": len(findings), "findings": findings}


if __name__ == "__main__":
    res = diff(Path(sys.argv[1]), Path(sys.argv[2]))
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != "findings"}, indent=2))
    for f in res["findings"]:
        print(f"- p{f['page']}: {f['evidence']}")

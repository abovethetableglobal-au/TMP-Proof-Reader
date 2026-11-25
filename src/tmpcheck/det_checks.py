"""Deterministic checks v0.2 (no LLM). Derived from REF-01 requirements RQ-01, RQ-05, RQ-06, RQ-14.

Usage: python -m src.tmpcheck.det_checks <submission.pdf> [out.json]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf

from .postprocess import locate, merge, set_outcome

PLACEHOLDERS = [
    ("PH-ANGLE", re.compile(r"<[^<>]{8,300}>", re.S), "Template instruction in <…> left in document", "Moderate"),
    ("PH-X", re.compile(r"\bX{2,}\b"), "Placeholder 'XX…' not completed", "Moderate"),
    ("PH-INSERT", re.compile(r"\[\s*insert[^\]]*\]?", re.I), "'[Insert …]' instruction left in document", "Moderate"),
    ("PH-TBA", re.compile(r"\bTB[AC]\b"), "'TBA/TBC' entry — confirm or complete before issue", "Minor"),
    ("PH-DATE", re.compile(r"(?<![\d])(?<!\d/)/\d{1,2}/20\d\d|(?<=\s)/20\d\d\b"), "Incomplete date (day or month missing)", "Moderate"),
]
# Interstate agencies/standards must never appear in a WA TMP (Tara, 2026-11-25, A-30): definite Moderate finding.
INTERSTATE = [
    ("JX-QLD", re.compile(r"\bTMR\b|Transport and Main Roads|\bQGTTM\b"), "Queensland agency/standard referenced (TMR/QGTTM) in a WA TMP"),
    ("JX-NSW", re.compile(r"\bTfNSW\b|Transport for NSW|\bRMS\b"), "NSW agency referenced in a WA TMP"),
    ("JX-VIC", re.compile(r"VicRoads|Department of Transport and Planning"), "Victorian agency referenced in a WA TMP"),
]
# Wording that may not belong in a WA local-government-road TMP (RQ-05). Raised as Query: context decides.
JURISDICTION = [
    ("JX-MRWA", re.compile(r"complex traffic management arrangements|Road Infrastructure Manager|State Roads?", re.I),
     "Main Roads / complex-arrangement wording — confirm it applies to this road and TMP type"),
]
# Run-together or split words and missing spaces that the AI passes miss on some runs (BENCH-04)
WORD_FORM = [
    ("WF-JOINED", re.compile(r"\b(upto|alot|infront|aswell|eachother|incase|inbetween|ontop)\b", re.I),
     "Words run together — should be two words (e.g. 'up to')"),
    ("WF-SPLIT", re.compile(r"\b\d+\s+(week|day|month|hour|year) s\b", re.I),
     "Word split by a stray space (e.g. 'week s' — should be 'weeks'' or 'weeks')"),
    ("WF-NOSPACE", re.compile(r"\b(No|Ref|Cert)\.(?=[A-Z0-9])"),
     "No space after the abbreviation's full stop"),
]
# Suggested action per rule (check 14 review: rule findings were issued with no action)
ACTIONS = {
    "PH-ANGLE": "Replace the template instruction with project-specific content, or delete it.",
    "PH-X": "Complete the placeholder.",
    "PH-INSERT": "Replace the '[Insert …]' instruction with project-specific content.",
    "PH-TBA": "Confirm and enter the value, or state when it will be confirmed.",
    "PH-DATE": "Enter the full date (day, month and year).",
    "JX-QLD": "Replace the reference with the WA (Main Roads WA) equivalent, or delete it.",
    "JX-NSW": "Replace the reference with the WA (Main Roads WA) equivalent, or delete it.",
    "JX-VIC": "Replace the reference with the WA (Main Roads WA) equivalent, or delete it.",
    "JX-MRWA": "Confirm the wording applies to this road and TMP type; delete it if it does not.",
    "WF-JOINED": "Separate the words (e.g. 'up to').",
    "WF-SPLIT": "Remove the stray space.",
    "WF-NOSPACE": "Add a space after the full stop.",
    "PG-HEADER": "Add the running header/footer to this page and check the page numbering that follows.",
    "DUP-SENT": "Check whether the repeat is intended; delete the duplicate if not.",
}
MAX_EV = 120
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
# TGS / drawing sheets carry title blocks and standard notes that legitimately repeat sheet to sheet.
# D5: SU_025 TGS 01/02 are portrait (US Letter inside an A4 TMP) with no "TGS" text, so orientation
# alone missed them. A page is a drawing if landscape, or it has >= 2 distinct title-block fields.
TITLE_BLOCK = re.compile(r"drawing\s*no|drawn\s*by|checked\s*by|designed\s*by|not\s*to\s*scale|\bscale\s*:|"
                         r"\bsheet\s*(?:no|\d)|\brev(?:ision)?\s*:", re.I)


def is_drawing(page) -> bool:
    if page.rect.width > page.rect.height:
        return True
    found = {re.sub(r"\W+", "", m.group(0).lower()) for m in TITLE_BLOCK.finditer(page.get_text())}
    return len(found) >= 2


def snippet(s: str, limit: int = MAX_EV) -> str:
    """Whitespace-collapsed evidence cut at a word boundary, marked with an ellipsis (no mid-word cuts)."""
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0] if " " in s[:limit] else s[:limit]
    return cut.rstrip(" ,;:") + "…"


def context(text: str, m, before: int, after: int) -> str:
    """Text around a match, widened to whole words at both ends."""
    a, b = max(0, m.start() - before), min(len(text), m.end() + after)
    while a > 0 and not text[a - 1].isspace():
        a -= 1
    while b < len(text) and not text[b].isspace():
        b += 1
    return text[a:b]


def page_list(pgs: list[int]) -> str:
    if len(pgs) == 1:
        return f"page {pgs[0]}"
    return "pages " + ", ".join(map(str, pgs[:-1])) + f" and {pgs[-1]}"


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def run(pdf: Path) -> dict:
    doc = pymupdf.open(pdf)
    pages = [p.get_text() for p in doc]
    # Drawing pages (TGSs, landscape) carry their own title block, not the TMP header (DEF-D02-1)
    drawing = {i for i, p in enumerate(doc, 1) if is_drawing(p)}
    findings = []

    def add(rule, page, evidence, issue, severity, category):
        f = {"rule": rule, "page": page, "evidence": snippet(evidence),
             "issue": issue, "severity": severity, "category": category, "action": ACTIONS.get(rule)}
        boxes = locate(doc[page - 1], f["evidence"])  # same locator as annotation (D1)
        if boxes:
            f["bbox"] = boxes
        findings.append(set_outcome(f))  # D3: Query -> "Unable to verify"

    for pno, text in enumerate(pages, 1):
        for rule, rx, issue, sev in PLACEHOLDERS:
            for m in rx.finditer(text):
                add(rule, pno, m.group(0), issue, sev, "C Completeness")
        for rule, rx, issue in WORD_FORM:
            for m in rx.finditer(text):
                add(rule, pno, context(text, m, 30, 30), issue, "Minor", "A Proofreading")
        for rule, rx, issue in INTERSTATE:
            for m in rx.finditer(text):
                add(rule, pno, context(text, m, 40, 40), issue + " — replace with the WA (Main Roads WA) equivalent",
                    "Moderate", "C Completeness")
        for rule, rx, issue in JURISDICTION:
            for m in rx.finditer(text):
                add(rule, pno, context(text, m, 40, 40), issue, "Query", "E Compliance")

    # Running header: the most common first line; pages without it (RQ-14)
    first_lines = [t.strip().split("\n")[0].strip() if t.strip() else "" for t in pages]
    header, freq = Counter(first_lines).most_common(1)[0]
    if freq >= len(pages) * 0.6:
        for pno, fl in enumerate(first_lines, 1):
            if fl != header and pno > 1 and pno not in drawing:
                add("PG-HEADER", pno, fl or "(no text)", "Page lacks the document's running header/footer — page numbering may be "
                    "out of step from here", "Minor", "A Presentation")

    # Repeated sentences (RQ-06): long sentences appearing more than once
    seen = defaultdict(list)
    for pno, text in enumerate(pages, 1):
        if pno in drawing:
            continue  # title blocks repeat by design across TGS sheets
        body = re.sub(r"\s+", " ", text)
        for s in SENT_SPLIT.split(body):
            k = norm(s)
            if len(k) >= 70:
                seen[k].append((pno, s.strip()))
    for k, occ in seen.items():
        pgs = sorted({p for p, _ in occ})
        if len(occ) > 1 and pgs[-1] - pgs[0] <= 6:  # nearby repeats (distant ones are often legitimate boilerplate)
            # Query (Owner, BENCH-01: repeats can be deliberate); category C (D5: duplicated text is completeness, RQ-06)
            where = page_list(pgs) if len(pgs) > 1 else f"twice on page {pgs[0]}" if len(occ) == 2 else f"{len(occ)} times on page {pgs[0]}"
            issue = f"Sentence repeated {len(occ)} times ({page_list(pgs)})" if len(pgs) > 1 else f"Sentence repeated {where}"
            add("DUP-SENT", pgs[0], occ[0][1], issue, "Query", "C Completeness")

    # DEF-C19-3: one TBA/TBC finding listing every page, not one per occurrence
    tba = [f for f in findings if f["rule"] == "PH-TBA"]
    if len(tba) > 1:
        pgs = sorted({f["page"] for f in tba})
        first = tba[0]
        first["related_pages"] = pgs[1:]
        first["issue"] = f"'TBA/TBC' entries ({len(tba)}) on {page_list(pgs)} — confirm or complete before issue"
        findings = [f for f in findings if f["rule"] != "PH-TBA" or f is first]

    for i, f in enumerate(findings, 1):
        f["id"] = f"F-{i:03d}"
    findings = merge(findings)  # D4
    return {"pages": len(pages), "findings": findings,
            "by_rule": dict(Counter(f["rule"] for f in findings))}


if __name__ == "__main__":
    res = run(Path(sys.argv[1]))
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(res, indent=2))
    print(json.dumps(res["by_rule"]))
    for f in res["findings"]:
        print(f"{f['id']} p{f['page']:<3}{f['rule']:<10}{f['evidence'][:95]}")

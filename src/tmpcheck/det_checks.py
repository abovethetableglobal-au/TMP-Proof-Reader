"""Deterministic checks v0.2 (no LLM). Derived from REF-01 requirements RQ-01, RQ-05, RQ-06, RQ-14.

Usage: python -m src.tmpcheck.det_checks <submission.pdf> [out.json]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf

PLACEHOLDERS = [
    ("PH-ANGLE", re.compile(r"<[^<>]{8,300}>", re.S), "Template instruction in <…> left in document", "Moderate"),
    ("PH-X", re.compile(r"\bX{2,}\b"), "Placeholder 'XX…' not completed", "Moderate"),
    ("PH-INSERT", re.compile(r"\[\s*insert[^\]]*\]?", re.I), "'[Insert …]' instruction left in document", "Moderate"),
    ("PH-TBA", re.compile(r"\bTB[AC]\b"), "'TBA/TBC' entry — confirm or complete before issue", "Minor"),
    ("PH-DATE", re.compile(r"(?<![\d])(?<!\d/)/\d{1,2}/20\d\d|(?<=\s)/20\d\d\b"), "Incomplete date (day or month missing)", "Moderate"),
]
# Wording that may not belong in a WA local-government-road TMP (RQ-05). Raised as Query: context decides.
JURISDICTION = [
    ("JX-QLD", re.compile(r"\bTMR\b|Transport and Main Roads|\bQGTTM\b"), "Queensland agency/standard referenced (TMR/QGTTM) in a WA TMP"),
    ("JX-NSW", re.compile(r"\bTfNSW\b|Transport for NSW|\bRMS\b"), "NSW agency referenced in a WA TMP"),
    ("JX-VIC", re.compile(r"VicRoads|Department of Transport and Planning"), "Victorian agency referenced in a WA TMP"),
    ("JX-MRWA", re.compile(r"complex traffic management arrangements|Road Infrastructure Manager|State Roads?", re.I),
     "Main Roads / complex-arrangement wording — confirm it applies to this road and TMP type"),
]
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


def run(pdf: Path) -> dict:
    doc = pymupdf.open(pdf)
    pages = [p.get_text() for p in doc]
    # Drawing pages (TGSs, landscape) carry their own title block, not the TMP header (DEF-D02-1)
    drawing = {i for i, p in enumerate(doc, 1) if p.rect.width > p.rect.height}
    findings = []

    def add(rule, page, evidence, issue, severity, category, outcome="Potential issue"):
        findings.append({"rule": rule, "page": page, "evidence": re.sub(r"\s+", " ", evidence)[:120],
                         "issue": issue, "severity": severity, "category": category, "outcome": outcome})

    for pno, text in enumerate(pages, 1):
        for rule, rx, issue, sev in PLACEHOLDERS:
            for m in rx.finditer(text):
                add(rule, pno, m.group(0), issue, sev, "C Completeness")
        for rule, rx, issue in JURISDICTION:
            for m in rx.finditer(text):
                add(rule, pno, text[max(0, m.start() - 40):m.end() + 40], issue, "Query", "E Compliance", "Unable to verify")

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
            # Query, not Minor: repeats can be deliberate (Owner excluded this type in BENCH-01; BENCH-02 action)
            add("DUP-SENT", pgs[0], occ[0][1], f"Sentence repeated {len(occ)} times (pages {', '.join(map(str, pgs))})",
                "Query", "A Proofreading", "Unable to verify")

    for i, f in enumerate(findings, 1):
        f["id"] = f"F-{i:03d}"
    return {"pages": len(pages), "findings": findings,
            "by_rule": dict(Counter(f["rule"] for f in findings))}


if __name__ == "__main__":
    res = run(Path(sys.argv[1]))
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(res, indent=2))
    print(json.dumps(res["by_rule"]))
    for f in res["findings"]:
        print(f"{f['id']} p{f['page']:<3}{f['rule']:<10}{f['evidence'][:95]}")

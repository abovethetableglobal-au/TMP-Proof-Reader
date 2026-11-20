"""WS6 technical spike S-01 — extraction, deterministic completeness checks, annotation.

Purpose: prove (1) page-level text extraction, (2) evidence-bound findings,
(3) annotated copy with numbered findings linked to a report, (4) original untouched.
No LLM, no customer data. Usage:
    python src/spike/completeness_spike.py <input.pdf> <out_dir>
"""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import pymupdf

# Placeholder patterns typical of unfinished templates (category C — completeness)
PATTERNS = [
    ("PH-DATE", re.compile(r"XX/XX/XX"), "Placeholder date not completed"),
    ("PH-X", re.compile(r"\bX{2,}\b"), "Placeholder 'XX…' not completed"),
    ("PH-DOTS", re.compile(r"^[….]{4,}:?$"), "Dotted blank field not completed"),  # whole word = dots only; excludes TOC leaders like "Crossings......" (DEF-S01-2)
    ("PH-INSERT", re.compile(r"\[\s*insert", re.I), "'[Insert …]' instruction left in document"),
]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(src: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    before = sha256(src)
    doc = pymupdf.open(src)
    # Word-level matching: each word has an exact bbox, so evidence and annotation
    # location come from the same source (fixes S-01 defect DEF-S01-1: substring
    # re-search produced duplicate/mis-labelled findings).
    unique = []
    for pno, page in enumerate(doc, start=1):
        words = page.get_text("words")  # x0,y0,x1,y1,word,block,line,wno
        current = None
        for x0, y0, x1, y1, w, b, ln, wn in words:
            hit = next(((c, d) for c, rx, d in PATTERNS if rx.search(w)), None)
            same_field = (current and hit and hit[0] == current["rule"]
                          and (b, ln) == current["_line"] and x0 - current["bbox"][2] < 25)
            if same_field:
                current["bbox"][2] = max(current["bbox"][2], x1)
                current["bbox"][3] = max(current["bbox"][3], y1)
                current["evidence"] = (current["evidence"] + " " + w)[:60]
                continue
            if current:
                unique.append(current)
                current = None
            if hit:
                code, desc = hit
                current = {
                    "id": "", "category": "C Completeness",
                    "severity": "Minor" if code == "PH-DOTS" else "Moderate",
                    "rule": code, "page": pno, "evidence": w[:60], "issue": desc,
                    "action": "Complete or remove the placeholder before issue.",
                    "outcome": "Potential issue", "bbox": [x0, y0, x1, y1], "_line": (b, ln),
                }
        if current:
            unique.append(current)
    for i, f in enumerate(unique, start=1):
        f["id"] = f"F-{i:03d}"
        f.pop("_line")
        f["bbox"] = [round(v, 1) for v in f["bbox"]]
        # Evidence validation: the quoted evidence must exist in the cited page's text
        assert f["evidence"].split()[0] in doc[f["page"] - 1].get_text(), f

    # Annotated rendition — on a copy; original never written
    ann = pymupdf.open(src)
    for f in unique:
        page = ann[f["page"] - 1]
        r = pymupdf.Rect(f["bbox"])
        h = page.add_rect_annot(r)  # red outline: distinguishable from template's own yellow highlighting (DEF-S01-3)
        h.set_colors(stroke=(0.85, 0, 0))
        h.set_border(width=1)
        h.set_info(title="TMP Check", content=f"{f['id']} [{f['severity']}] {f['issue']}")
        h.update()
        page.insert_text((r.x1 + 1, r.y0 + 6), f["id"], fontsize=6, color=(0.8, 0, 0))
    ann_path = out / (src.stem + "_ANNOTATED.pdf")
    ann.save(ann_path)

    after = sha256(src)
    result = {
        "source": src.name,
        "pages": doc.page_count,
        "findings": len(unique),
        "by_severity": {s: sum(f["severity"] == s for f in unique) for s in ("Moderate", "Minor")},
        "original_unchanged": before == after,
        "seconds": round(time.time() - t0, 2),
        "annotated_pdf": ann_path.name,
    }
    (out / "findings.json").write_text(json.dumps({"summary": result, "findings": unique}, indent=2))
    lines = [f"# Spike S-01 report — {src.name}", "",
             "AI-assisted document QA spike. Not an approval or compliance declaration.", "",
             "| Measure | Value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in result.items()]
    lines += ["", "| ID | Page | Severity | Evidence | Issue |", "|---|---|---|---|---|"]
    lines += [f"| {f['id']} | {f['page']} | {f['severity']} | `{f['evidence']}` | {f['issue']} |" for f in unique]
    (out / "report.md").write_text("\n".join(lines) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1]), Path(sys.argv[2])), indent=2))

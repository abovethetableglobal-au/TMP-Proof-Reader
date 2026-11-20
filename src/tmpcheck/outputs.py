"""Output 1 (TMP Check Report PDF, D-11) and Output 2 (annotated TMP, D-12) — Handover §6.

Both outputs are built from the same numbered finding list, so F-numbers match.
- Draft outputs are watermarked DRAFT; finals are produced only after the accredited reviewer has
  dispositioned every finding (A-15). Rejected findings are left out of the final.
- The customer's original is never modified: the annotated copy is a separate file, annotations only,
  with no pages added or removed (pagination preserved).
- Wording follows CLAUDE.md §2: never "approved", "compliant", "safe" or "100%".

Uses PyMuPDF only (no extra dependency).
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pymupdf

SEVERITIES = ["Critical", "Major", "Moderate", "Minor", "Query"]
SEV_RANK = {s: i for i, s in enumerate(SEVERITIES)}
SEV_COLOUR = {"Critical": (0.71, 0.14, 0.09), "Major": (0.88, 0.48, 0.04), "Moderate": (0.79, 0.54, 0.02),
              "Minor": (0.11, 0.31, 0.85), "Query": (0.40, 0.44, 0.52)}
SEV_HEX = {"Critical": "#b42318", "Major": "#e07a0a", "Moderate": "#ca8a04", "Minor": "#1d4ed8", "Query": "#667085"}

SCOPE = [
    ("A", "Proofreading and presentation", "Spelling, grammar, punctuation, wording, units and style consistency."),
    ("B", "Document consistency", "Dates, durations, hours, speeds, counts, stages, roles, contacts, cross-references "
                                  "and risk scores compared across the TMP, appendices and drawings."),
    ("C", "Completeness and template leftovers", "Template instructions, blank fields, empty registers, missing "
                                                 "appendices, wording from other authorities or TMP types."),
    ("D", "TGS and figure cross-check", "Title blocks, sign schedules, notes and labels on the TGS drawings and "
                                        "figures compared with the TMP text."),
    ("E", "Selected WA requirements", "Rules from the reviewed compliance reference library. A potential issue is "
                                      "raised only where a rule is cited; otherwise it is a Query."),
]

LIMITATIONS = [
    "TMP Check is an AI-assisted document quality check. It is not an approval, certification, design review, "
    "engineering assessment, site inspection or safety declaration, and it does not replace road authority approval.",
    "Findings are potential issues for the accredited reviewer to assess. 'No issue identified in this check' means "
    "only that this check did not identify one; it does not mean that none exists.",
    "Automated checks can miss issues, and results can vary between runs. The organisation's accredited reviewer "
    "remains responsible for the professional assessment, correction, endorsement and submission of the TMP.",
    "Drawing checks are made from the PDF at drawing scale. Findings marked VISUAL describe what is visible and "
    "need confirmation by the reviewer.",
    "Severity ratings are prioritisation aids, not formal risk assessments.",
    "Compliance findings are limited to the rules in the compliance reference library listed in this report.",
]


@dataclass
class Item:
    no: str
    severity: str
    page: int
    pages: list[int]
    category: str
    issue: str
    evidence: str
    action: str
    outcome: str
    rule: str
    source: str
    disposition: str
    reviewer_note: str
    annotated: str = ""          # "highlighted" | "note" — set by annotate()


@dataclass
class Meta:
    doc_ref: str
    filename: str
    organisation: str
    pages: int | None
    uploaded: datetime
    final: bool
    reviewer: str = ""
    final_date: datetime | None = None
    ai_passes: str = ""
    sources: list[dict] = field(default_factory=list)   # [{name, edition, authority, count}]


def number_findings(rows: list[dict], final: bool) -> list[Item]:
    """Order by severity then page; drop reviewer-rejected findings from a final."""
    keep = [r for r in rows if not (final and r.get("disposition") == "rejected")]
    keep.sort(key=lambda r: (SEV_RANK.get(r.get("severity"), 9), int(r.get("page") or 1), r.get("id") or 0))
    items = []
    for i, r in enumerate(keep, 1):
        pages = sorted({int(p) for p in str(r.get("pages") or r.get("page") or 1).replace(" ", "").split(",") if p})
        items.append(Item(no=f"F-{i:03d}", severity=r.get("severity") or "Query", page=int(r.get("page") or 1),
                          pages=pages, category=r.get("category") or "", issue=r.get("issue") or "",
                          evidence=r.get("evidence") or "", action=r.get("action") or "",
                          outcome=r.get("outcome") or "Potential issue", rule=r.get("rule") or "",
                          source=r.get("source") or "", disposition=r.get("disposition") or "pending",
                          reviewer_note=r.get("reviewer_note") or ""))
    return items


# ---------------------------------------------------------------------------- report (Output 1)

def _e(s) -> str:
    return html.escape(str(s or "")).replace("\n", "<br>")


def _date(d: datetime | None) -> str:
    return f"{d.day} {d:%B %Y}" if d else "—"


CSS = """
* { font-family: sans-serif; }
body { font-size: 9pt; color: #101828; }
h1 { font-size: 18pt; color: #14233f; margin: 0 0 2pt 0; }
h2 { font-size: 12pt; color: #14233f; margin: 14pt 0 4pt 0; border-bottom: 1px solid #f28c1b; }
h3 { font-size: 10pt; margin: 10pt 0 3pt 0; }
p { margin: 2pt 0 4pt 0; }
table { border-collapse: collapse; width: 100%; }
td, th { border: 1px solid #d0d5dd; padding: 3pt; vertical-align: top; text-align: left; }
th { background-color: #f2f4f7; }
.sub { color: #475467; }
.small { font-size: 8pt; color: #475467; }
.ev { font-style: italic; color: #344054; }
"""


def _sev_cell(s: str) -> str:
    return f'<b style="color:{SEV_HEX.get(s, "#344054")}">{_e(s)}</b>'


def report_html(meta: Meta, items: list[Item], all_rows: list[dict]) -> str:
    status = "FINAL" if meta.final else "DRAFT — for review by the accredited reviewer"
    counts = {s: sum(1 for i in items if i.severity == s) for s in SEVERITIES}
    h = [f"<h1>TMP Check Report</h1><p class='sub'><b>{_e(status)}</b></p>"]

    h.append("<h2>1. Project and document</h2><table>")
    rows = [("Document", meta.doc_ref), ("File", meta.filename), ("Organisation", meta.organisation),
            ("Pages checked", meta.pages or "—"), ("Date submitted", _date(meta.uploaded)),
            ("Report status", "Final" if meta.final else "Draft"),
            ("Reviewer", meta.reviewer if meta.final else "Not yet reviewed"),
            ("Final issued", _date(meta.final_date) if meta.final else "—")]
    h += [f"<tr><th width='28%'>{_e(k)}</th><td>{_e(v)}</td></tr>" for k, v in rows]
    h.append("</table>")

    h.append("<h2>2. Checking scope</h2><table><tr><th width='6%'>Cat.</th><th width='28%'>Check</th><th>Covers</th></tr>")
    h += [f"<tr><td>{c}</td><td>{_e(n)}</td><td>{_e(d)}</td></tr>" for c, n, d in SCOPE]
    h.append("</table>")
    h.append(f"<p class='small'>Automated rule checks and AI checking passes{(' (' + _e(meta.ai_passes) + ')') if meta.ai_passes else ''} "
             "were run. Every AI finding quotes text from the cited page; findings whose quote could not be found on "
             "the page are reported as Query.</p>")

    h.append("<h2>3. Compliance reference sources</h2>")
    if meta.sources:
        h.append("<table><tr><th>Source</th><th width='18%'>Edition</th><th width='22%'>Authority</th><th width='10%'>Rules</th></tr>")
        h += [f"<tr><td>{_e(s['name'])}</td><td>{_e(s['edition'])}</td><td>{_e(s['authority'])}</td><td>{s['count']}</td></tr>"
              for s in meta.sources]
        h.append("</table>")
    else:
        h.append("<p>No compliance rules were applied.</p>")

    h.append("<h2>4. Summary</h2><table><tr>" + "".join(f"<th>{s}</th>" for s in SEVERITIES) + "<th>Total</th></tr><tr>"
             + "".join(f"<td>{counts[s]}</td>" for s in SEVERITIES) + f"<td>{len(items)}</td></tr></table>")
    if meta.final:
        rejected = sum(1 for r in all_rows if r.get("disposition") == "rejected")
        edited = sum(1 for i in items if i.disposition == "edited")
        h.append(f"<p>The accredited reviewer assessed every finding raised. {len(items)} are included in this report "
                 f"({edited} edited by the reviewer); {rejected} {'was' if rejected == 1 else 'were'} rejected by the reviewer "
                 "and not included.</p>")
    else:
        h.append("<p>This is a draft. Each finding must be accepted, edited or rejected by the organisation's accredited "
                 "reviewer before a final report is issued.</p>")
    top = [i for i in items if i.severity in ("Critical", "Major")][:10]
    if top:
        h.append("<h3>Most significant potential issues</h3><ul>")
        h += [f"<li><b>{i.no}</b> ({_e(i.severity)}, p{', '.join(map(str, i.pages))}): {_e(i.issue)}</li>" for i in top]
        h.append("</ul>")
    if not items:
        h.append("<p><b>No issue identified in this check.</b></p>")

    h.append("<h2>5. Findings</h2>")
    for s in SEVERITIES:
        group = [i for i in items if i.severity == s]
        if not group:
            continue
        h.append(f"<h3>{_e(s)} ({len(group)})</h3><table><tr><th width='8%'>No.</th><th width='9%'>Page</th>"
                 "<th>Finding</th><th width='30%'>Suggested action</th></tr>")
        for i in group:
            meta_line = " · ".join(x for x in [i.category, i.outcome, f"rule {i.rule}" if i.rule else ""] if x)
            body = f"{_e(i.issue)}"
            if i.evidence:
                body += f"<br><span class='ev'>Evidence: “{_e(i.evidence[:600])}”</span>"
            body += f"<br><span class='small'>{_e(meta_line)}</span>"
            if meta.final and i.disposition == "edited" and i.reviewer_note:
                body += f"<br><b>Reviewer edit:</b> {_e(i.reviewer_note)}"
            elif meta.final and i.reviewer_note:
                body += f"<br><span class='small'>Reviewer note: {_e(i.reviewer_note)}</span>"
            h.append(f"<tr><td>{i.no}</td><td>{', '.join(map(str, i.pages))}</td><td>{body}</td>"
                     f"<td>{_e(i.action) or '—'}</td></tr>")
        h.append("</table>")

    review = [i for i in items if i.severity == "Query" or i.evidence.upper().startswith("VISUAL:")]
    h.append("<h2>6. Matters requiring human review</h2>")
    if review:
        h.append("<p>These findings could not be verified from the document text alone (Query) or describe a drawing "
                 "as seen (VISUAL). The reviewer should confirm each one.</p><p>"
                 + ", ".join(i.no for i in review) + "</p>")
    else:
        h.append("<p>None beyond the reviewer's assessment of every finding.</p>")
    note_only = [i.no for i in items if i.annotated == "note"]
    if note_only:
        h.append("<p class='small'>In the annotated copy, these findings are marked with a note at the top of the page "
                 "rather than a highlight, because the exact text could not be located: " + ", ".join(note_only) + ".</p>")

    h.append("<h2>7. Limitations and exclusions</h2><ul>" + "".join(f"<li>{_e(x)}</li>" for x in LIMITATIONS) + "</ul>")
    return "".join(h)


def _decorate(path: Path, meta: Meta) -> None:
    doc = pymupdf.open(path)
    n = doc.page_count
    for k, page in enumerate(doc, 1):
        w, h = page.rect.width, page.rect.height
        page.insert_text((40, 30), f"TMP Check Report · {meta.doc_ref}", fontsize=7.5, color=(0.4, 0.44, 0.52))
        page.insert_text((w - 110, h - 22), f"Page {k} of {n}", fontsize=7.5, color=(0.4, 0.44, 0.52))
        page.insert_text((40, h - 22), "Document quality check only — not an approval or certification.",
                         fontsize=7.5, color=(0.4, 0.44, 0.52))
        if not meta.final:
            page.insert_text((120, h / 2 + 120), "DRAFT", fontsize=110, color=(0.85, 0.85, 0.85),
                             morph=(pymupdf.Point(w / 2, h / 2), pymupdf.Matrix(-35)), overlay=False)
    doc.saveIncr()
    doc.close()


def build_report(meta: Meta, items: list[Item], all_rows: list[dict], out: Path) -> Path:
    story = pymupdf.Story(html=report_html(meta, items, all_rows), user_css=CSS)
    writer = pymupdf.DocumentWriter(str(out))
    box = pymupdf.paper_rect("a4")
    where = box + (40, 45, -40, -45)
    more = True
    while more:
        dev = writer.begin_page(box)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()
    _decorate(out, meta)
    return out


# ---------------------------------------------------------------------------- annotated copy (Output 2)

def _locate(page: pymupdf.Page, evidence: str) -> list:
    text = re.sub(r"\s+", " ", evidence or "").strip().strip("“”\"'")
    if not text or text.upper().startswith("VISUAL:"):
        return []
    if len(text) < 6:                                       # short evidence (e.g. 'TBA', '/2026'): exact only
        return page.search_for(text, quads=True)
    for n in (len(text), 80, 50, 30, 18):
        needle = text[:n].strip()
        if len(needle) < 6:
            break
        quads = page.search_for(needle, quads=True)
        if quads:
            return quads
        for part in re.split(r" \| |\n", needle):          # multi-line quotes: try the first line on its own
            if len(part) >= 12 and (q := page.search_for(part.strip(), quads=True)):
                return q
    return []


def _label(page: pymupdf.Page, rect: pymupdf.Rect, text: str, colour) -> None:
    rect = rect * page.derotation_matrix
    a = page.add_freetext_annot(rect, text, fontsize=6.5, text_color=colour, fill_color=(1, 1, 1))
    a.set_border(width=0.6)
    a.set_info(title="TMP Check", content=text)
    a.update()


def annotate(original: Path, items: list[Item], out: Path, final: bool) -> Path:
    """Write annotations onto a copy of the original. Returns the output path."""
    doc = pymupdf.open(original)
    stack: dict[int, int] = {}
    row_count: dict[tuple, int] = {}

    def margin_note(pno: int, text: str, colour) -> None:
        page = doc[pno - 1]
        k = stack.get(pno, 0)
        stack[pno] = k + 1
        w = page.rect.width
        _label(page, pymupdf.Rect(w - 150, 8 + k * 13, w - 6, 20 + k * 13), text, colour)

    for i in items:
        colour = SEV_COLOUR.get(i.severity, (0.4, 0.44, 0.52))
        summary = f"{i.no} [{i.severity}] {i.issue}"
        if i.action:
            summary += f"\nSuggested action: {i.action}"
        if not 1 <= i.page <= doc.page_count:
            continue
        page = doc[i.page - 1]
        quads = _locate(page, i.evidence)
        if quads:
            hl = page.add_highlight_annot(quads)
            hl.set_colors(stroke=colour)
            hl.set_opacity(0.35)
            hl.set_info(title="TMP Check", content=summary)
            hl.update()
            r = quads[0].rect
            row = (i.page, round(r.y0 / 6))                          # labels sit in the left margin,
            x0 = 3 + 33 * row_count.get(row, 0)                       # side by side if a line has several
            row_count[row] = row_count.get(row, 0) + 1
            _label(page, pymupdf.Rect(x0, r.y0, x0 + 31, r.y0 + 9), i.no, colour)
            i.annotated = "highlighted"
        else:
            margin_note(i.page, f"{i.no} {i.severity} — see report", colour)
            i.annotated = "note"
        for p in i.pages:
            if p != i.page and 1 <= p <= doc.page_count:
                margin_note(p, f"{i.no} (related) — see report", colour)

    first = doc[0]
    banner = ("TMP Check annotated copy — FINAL. Annotations only; original content unchanged."
              if final else "TMP Check annotated copy — DRAFT for reviewer. Annotations only; original content unchanged.")
    _label(first, pymupdf.Rect(6, 6, min(first.rect.width - 160, 420), 18), banner, (0.08, 0.14, 0.25))
    doc.save(out, garbage=3, deflate=True)
    doc.close()
    return out

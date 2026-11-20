"""Generate SAMPLE-TMP-01.pdf — a synthetic, fictitious TMP with known seeded issues.

No customer data. Used to test the portal end to end.
    python test-library/samples/make_sample_tmp.py
Seeded issues (expected from deterministic checks):
  - '<Insert ...>' template instruction left in (p2)          Moderate
  - 'XXXX' placeholder (p3)                                   Moderate
  - 'TBC' entry (p3)                                          Minor
  - Queensland 'TMR' reference in a WA TMP (p4)               Query
  - Incomplete date '/2026' (p2)                              Moderate
  - Page without the running header (p5)                      Minor
  - Sentence repeated on nearby pages (p3, p4)                Minor
"""
from pathlib import Path

import pymupdf

HEADER = "Traffic Management Plan - Sample Street Resurfacing - Rev A"
REPEAT = ("All traffic controllers must hold current accreditation and wear high visibility clothing "
          "at all times while on the worksite.")
PAGES = [
    ["TRAFFIC MANAGEMENT PLAN", "Project: Sample Street Resurfacing (fictitious)", "Road authority: City of Example",
     "Prepared by: Example Traffic Pty Ltd", "This document is a synthetic test sample. It contains no real project data."],
    ["1 Introduction", "Works will be carried out on Sample Street between Alpha Road and Beta Avenue.",
     "Date of works: /2026", "<Insert a description of the works and the staging sequence here>"],
    ["2 Roles and Responsibilities", "Traffic management implementer: XXXX", "Site contact phone: TBC.", REPEAT],
    ["3 Traffic Arrangements", "Signage will be installed in accordance with TMR requirements.", REPEAT,
     "A single lane will remain open to traffic in each direction."],
    ["4 Pedestrian Management", "Footpath access will be maintained on the northern side at all times."],
]


def main(out: Path = Path(__file__).with_name("SAMPLE-TMP-01.pdf")) -> Path:
    doc = pymupdf.open()
    for i, lines in enumerate(PAGES, 1):
        page = doc.new_page(width=595, height=842)
        y = 60
        if i != 5:                       # page 5 deliberately lacks the running header
            page.insert_text((50, 40), HEADER, fontsize=9)
        for ln in lines:
            rect = pymupdf.Rect(50, y, 545, y + 80)
            page.insert_textbox(rect, ln, fontsize=11)
            y += 24 + 14 * (len(ln) // 85)
        page.insert_text((280, 820), f"Page {i}", fontsize=9)
    tgs = doc.new_page(width=842, height=595)   # landscape drawing page (TGS)
    tgs.insert_text((50, 50), "TGS 01 - Sample Street lane closure (fictitious drawing)", fontsize=12)
    tgs.draw_rect(pymupdf.Rect(50, 80, 790, 540), color=(0, 0, 0))
    doc.save(out)
    return out


if __name__ == "__main__":
    print(main())

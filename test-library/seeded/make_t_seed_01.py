"""Rebuild T-SEED-01 from the public MRWA template (PUB-01). Run from repo root."""
import json
from docx import Document

REMOVE = {"Shadow Vehicles", "Rail Crossings", "Fog, Dust and Smoke"}  # expected missing-heading findings
RENAME = {"Night time Provisions": "Night-time Provisions"}             # minor variation: must NOT be flagged

d = Document("test-library/public/mrwa-tmp-template.docx")
for p in list(d.paragraphs):
    t = p.text.strip()
    if p.style.name.startswith("Heading") and t in REMOVE:
        p._element.getparent().remove(p._element)
    elif p.style.name.startswith("Heading") and t in RENAME:
        for r in p.runs:
            r.text = ""
        p.runs[0].text = RENAME[t]
d.save("test-library/seeded/T-SEED-01.docx")
json.dump({"doc": "T-SEED-01", "rule": "WA-COP-4.2.1-001", "expected_missing": sorted(REMOVE),
           "must_not_flag": list(RENAME.values()),
           "note": "TOC not refreshed: deleted headings still appear in table of contents (tests TOC exclusion)"},
          open("test-library/seeded/T-SEED-01.expected.json", "w"), indent=2)
# then: cd test-library/seeded && soffice --headless --convert-to pdf T-SEED-01.docx

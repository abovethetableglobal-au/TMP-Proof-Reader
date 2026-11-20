"""LLM checking passes (categories A, B, C-semantic, D) — Claude API.

Design
- One TMP PDF sent once as a `document` block (text + page images, so TGS drawings are seen),
  cached with `cache_control`; each pass reuses the cached prefix and adds its own instructions.
- Structured output (Pydantic) — every finding has page, quoted evidence, issue, fix.
- Evidence validation: a text finding's quote must exist on the cited PDF page, else it is
  downgraded to a Query (never silently released as a confirmed issue — CLAUDE.md §2).
- Server-side refusal fallback enabled; usage and cost recorded per pass.

Requires ANTHROPIC_API_KEY. Approved use: A-16 / A-18 (historical WTGTM documents).
Usage: python -m src.tmpcheck.llm_checks <tmp.pdf> <out.json> [--passes A,B,C,D] [--dry-run]
"""
import argparse
import base64
import json
import re
import sys
import time
from pathlib import Path
from typing import List, Literal, Optional

import anthropic
import pymupdf
from pydantic import BaseModel, Field

MODEL = "claude-opus-5-5"
EFFORT = "high"            # intelligence-sensitive QA work
MAX_TOKENS = 64000         # streaming, so large output (many findings + thinking) is safe
BETAS = ["server-side-fallback-2026-07-01"]
# USD per million tokens for claude-opus-5-5 (skill table, cached 2026-11-03). Cache write = 1.25x input (5-min TTL).
PRICE = {"input": 4.00, "output": 20.00, "cache_read": 0.20, "cache_write": 5.00}


class Finding(BaseModel):
    page: int = Field(description="PDF page number (1-based) where the issue appears")
    section: str = Field(description="Section number/heading, or 'Cover', 'TGS 01', 'Appendix A' etc.")
    evidence: str = Field(description="Exact text copied from the page that shows the issue (max ~25 words). "
                                      "For drawing-only issues with no selectable text, describe what is visible, prefixed 'VISUAL:'")
    issue: str = Field(description="What is wrong, in one sentence")
    fix: str = Field(description="Suggested correction or action")
    severity: Literal["Critical", "Major", "Moderate", "Minor", "Query"]
    related_pages: List[int] = Field(default_factory=list, description="Other pages involved (for consistency issues)")


class PassResult(BaseModel):
    findings: List[Finding]
    open_questions: List[str] = Field(default_factory=list,
                                      description="Questions for the TMP designer where facts conflict and the correct value cannot be determined")


SYSTEM = """You are a meticulous quality checker of Western Australian Traffic Management Plans (TMPs) for works on roads.
You check documents; you do not approve, certify or endorse them, and you never state that a document is compliant or safe.
Rules:
- Report only issues you can point to in the document. Never invent site conditions or technical corrections.
- 'evidence' must be copied exactly from the cited page (same spelling and punctuation), or start with 'VISUAL:' for drawing-only issues.
- Use PDF page numbers (the first page of the file is page 1), not printed footer numbers.
- Use Australian English.
- The Main Roads WA TMP template requires its section headings to be retained, including the template's own heading
  wording (e.g. 'Existing Traffic and Adverting Signs'). Do not report template-mandated heading text as an error.
- Severity: Critical = potential serious safety or mandatory-requirement issue; Major = significant technical/completeness concern;
  Moderate = important inconsistency or ambiguity; Minor = editorial/presentation; Query = cannot verify from the document.
- Be thorough: a typical 60-page TMP contains dozens of genuine issues. Report every instance, not a sample."""

PASSES = {
    "A": ("Proofreading and presentation",
          "Check spelling, grammar, punctuation, sentence clarity, capitalisation, abbreviations and units "
          "(e.g. '60km/h' vs '60 km/h', 'AS1742.3' vs 'AS 1742.3:2019'), heading wording, and wrong words. "
          "Report each error individually. Also list inconsistent variants of the same term (e.g. car park/carpark) "
          "as one Minor finding per term, giving the variants in 'evidence'."),
    "B": ("Document consistency",
          "Cross-check facts across the whole document, appendices and TGS drawings: project dates and duration, hours and "
          "days of work, revision numbers and dates (including TGS dates vs site inspection date), vehicle and traffic "
          "counts and volumes, speeds, setbacks and device sizes, stage numbering, role titles, names and contact details, "
          "contents page vs actual headings and page numbers, internal cross-references ('see 7.3.2'), and risk scores "
          "(recalculate Likelihood x Consequence and the rating band against the TMP's own matrix). "
          "For each conflict cite one page in 'page' and the others in 'related_pages'. Put unresolved conflicts in open_questions."),
    "C": ("Completeness and template leftovers",
          "Find template instructions or example text left in, blank fields and table cells, empty registers, sections "
          "that say 'N/A' but are later described as applicable (or vice versa), statements that contradict each other, "
          "duplicated paragraphs, text placed under the wrong heading, wording that belongs to a different road authority, "
          "state or TMP type (e.g. Main Roads 'complex traffic arrangements' wording in a local-road TMP, Queensland 'TMR'), "
          "documents referred to that are not included, and missing appendices or evidence."),
    "D": ("TGS drawings and figures",
          "Look at every TGS drawing and figure as an image. Compare title blocks (date, revision, duration, company name, "
          "sign quantities) with the TMP text; check signs and devices described in the text appear on the plan; check "
          "labels and notes against the text (tolerances, cone spacing, aftercare); and report text or symbols clipped by "
          "the drawing frame. Use 'VISUAL:' evidence where the drawing has no selectable text."),
}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s.lower())).strip()


def validate(findings: list[dict], page_text: list[str]) -> None:
    """Evidence validation: quote must appear on the cited page (or a related page)."""
    for f in findings:
        ev = f["evidence"]
        if ev.upper().startswith("VISUAL:"):
            f["evidence_check"] = "visual — reviewer to confirm"
            continue
        key = norm(ev)
        pages = [f["page"], *f.get("related_pages", [])]
        hit = next((p for p in pages if 1 <= p <= len(page_text) and key and key in norm(page_text[p - 1])), None)
        if hit is None:  # tolerate a short off-by-one in page attribution
            hit = next((p for p in (f["page"] - 1, f["page"] + 1) if 1 <= p <= len(page_text) and key and key in norm(page_text[p - 1])), None)
            if hit:
                f["page"] = hit
        if hit:
            f["evidence_check"] = "verified"
        else:
            f["evidence_check"] = "NOT FOUND on cited page"
            f["original_severity"], f["severity"] = f["severity"], "Query"   # never release unsupported findings as confirmed


def cost(u) -> float:
    return ((u.input_tokens or 0) * PRICE["input"] + (u.output_tokens or 0) * PRICE["output"]
            + (getattr(u, "cache_read_input_tokens", 0) or 0) * PRICE["cache_read"]
            + (getattr(u, "cache_creation_input_tokens", 0) or 0) * PRICE["cache_write"]) / 1e6


def run(pdf: Path, passes: list[str], dry_run: bool = False) -> dict:
    data = base64.standard_b64encode(pdf.read_bytes()).decode()
    page_text = [p.get_text() for p in pymupdf.open(pdf)]
    doc_block = {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data},
                 "title": pdf.name, "cache_control": {"type": "ephemeral"}}
    client = anthropic.Anthropic()
    out = {"model": MODEL, "effort": EFFORT, "passes": {}, "usd_total": 0.0}
    for code in passes:
        name, instructions = PASSES[code]
        req = dict(model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM,
                   output_config={"effort": EFFORT}, output_format=PassResult,
                   betas=BETAS, fallbacks="default",
                   messages=[{"role": "user", "content": [doc_block, {"type": "text", "text": f"Check pass {code} — {name}.\n{instructions}"}]}])
        if dry_run:
            print(f"[dry-run] pass {code}: request built ({len(data)//1024} KB PDF)"); continue
        t0 = time.time()
        try:
            with client.beta.messages.stream(**req) as stream:
                msg = stream.get_final_message()
        except anthropic.RateLimitError as e:
            print(f"pass {code}: rate limited — {e.message}", file=sys.stderr); raise
        except anthropic.APIStatusError as e:
            print(f"pass {code}: API error {e.status_code} — {e.message}", file=sys.stderr); raise
        if msg.stop_reason == "refusal":
            out["passes"][code] = {"error": "refusal", "stop_details": str(msg.stop_details)}; continue
        if msg.stop_reason == "max_tokens":
            print(f"pass {code}: hit max_tokens — output may be incomplete", file=sys.stderr)
        text = next(b.text for b in msg.content if b.type == "text")
        res = PassResult.model_validate_json(text).model_dump()
        for f in res["findings"]:
            f["pass"] = code
        validate(res["findings"], page_text)
        u = msg.usage
        res["usage"] = {"input": u.input_tokens, "output": u.output_tokens,
                        "cache_read": getattr(u, "cache_read_input_tokens", 0),
                        "cache_write": getattr(u, "cache_creation_input_tokens", 0),
                        "usd": round(cost(u), 4), "seconds": round(time.time() - t0, 1), "stop_reason": msg.stop_reason}
        out["usd_total"] += res["usage"]["usd"]
        out["passes"][code] = res
        print(f"pass {code}: {len(res['findings'])} findings, ${res['usage']['usd']:.2f}, {res['usage']['seconds']}s, "
              f"cache read {res['usage']['cache_read']}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("out")
    ap.add_argument("--passes", default="A,B,C,D"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    res = run(Path(a.pdf), a.passes.split(","), a.dry_run)
    if not a.dry_run:
        Path(a.out).write_text(json.dumps(res, indent=2))
        print(f"total ${res['usd_total']:.2f} USD")

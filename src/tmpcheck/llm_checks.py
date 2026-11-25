"""LLM checking passes (categories A, B, C-semantic, D) — Claude API.

Design
- One TMP PDF sent once as a `document` block (text + page images, so TGS drawings are seen),
  cached with `cache_control`; each pass reuses the cached prefix and adds its own instructions.
- Structured output (Pydantic) — every finding has page, quoted evidence, issue, fix.
- Evidence validation (postprocess.py): a quote must be locatable word-by-word on the cited page
  (same locator as annotation), else Query / 'Unable to verify'; VISUAL-only Criticals held as Query;
  duplicates across passes merged (CLAUDE.md §2).
- Server-side refusal fallback enabled; usage and cost recorded per pass.

Requires ANTHROPIC_API_KEY. Approved use: A-16 / A-18 (historical WTGTM documents).
Usage: python -m src.tmpcheck.llm_checks <tmp.pdf> <out.json> [--passes A,B,C,D] [--dry-run]
"""
import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import List, Literal, Optional

import anthropic
import pymupdf
from pydantic import BaseModel, Field

from .postprocess import merge, validate

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
- This is a Western Australian document. Never cite, recommend or apply another state's agency, standard or practice
  (e.g. Queensland TMR/MUTCD/QGTTM, Transport for NSW, VicRoads) in 'issue' or 'fix'. Cite only Main Roads WA, the WA
  Code of Practice and the AGTTM/AS editions it adopts. Interstate wording found IN the document is itself a finding.
- The Main Roads WA TMP template requires its section headings to be retained, including the template's own heading
  wording (e.g. 'Existing Traffic and Adverting Signs'). Do not report template-mandated heading text as an error.
- Severity: Critical = potential serious safety or mandatory-requirement issue; Major = significant technical/completeness concern;
  Moderate = important inconsistency or ambiguity; Minor = editorial/presentation; Query = cannot verify from the document.
- Be thorough: a typical 60-page TMP contains dozens of genuine issues. Report every distinct error, not a sample.
- Report each underlying problem once. If the same conflict or omission shows on several pages, report it at the
  first page and list the other pages in 'related_pages'; do not raise it again for each page."""

PASSES = {
    "A": ("Proofreading and presentation",
          "Check spelling, grammar, punctuation, sentence clarity, capitalisation, abbreviations and units "
          "(e.g. '60km/h' vs '60 km/h', 'AS1742.3' vs 'AS 1742.3:2019'), heading wording, and wrong words. "
          "Report each error individually. Work through this punctuation checklist on every page, including bullets, "
          "table cells and the last sentence of each section: missing full stop at the end of a sentence; double or stray "
          "punctuation (';.', '. -', ':-', '20 km/h.'); missing space after a full stop or before a unit; words run "
          "together or split ('upto', 'week s'); missing apostrophes ('2 weeks notice'); stray spaces in headings "
          "('Constraint /Impacts'); a term defined twice. "
          "Style consistency is different: do NOT report unit spacing, capitalisation, hyphenation, dash style, time or "
          "date formats, or term variants (e.g. car park/carpark, Prestart/pre-start) instance by instance. Give ONE Minor "
          "finding per term, listing every variant in 'evidence' and the pages in 'related_pages'."),
    "B": ("Document consistency",
          "Cross-check facts across the whole document, appendices and TGS drawings: project dates and duration, hours and "
          "days of work, revision numbers and dates (including TGS dates vs site inspection date), vehicle and traffic "
          "counts and volumes, speeds, setbacks and device sizes, stage numbering, role titles, names and contact details, "
          "contents page vs actual headings and page numbers, internal cross-references ('see 7.3.2'), and risk scores "
          "(recalculate Likelihood x Consequence and the rating band against the TMP's own matrix). "
          "For each conflict cite one page in 'page' and the others in 'related_pages', and report the conflict once only. "
          "Put unresolved conflicts in open_questions."),
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
          "the drawing frame. Also check body figures and site photos (e.g. Figure 1 and 2): captions, dates and photo "
          "order against the text. Judgements about where an item sits on an aerial photo or plan (e.g. whether a truck is "
          "on a path, or whether spacing meets a tolerance) are uncertain at drawing scale: report them as Query unless "
          "unmistakable, and do not contradict a note on the drawing that is consistent with the TMP text. "
          "Use 'VISUAL:' evidence where the drawing has no selectable text."),
}


INTERSTATE_RX = re.compile(r"Queensland|\bQLD\b|\bTMR\b|QGTTM|\bMUTCD\b|New South Wales|\bNSW\b|TfNSW|Victoria|VicRoads", re.I)


def jurisdiction_guard(findings: list[dict]) -> None:
    """Our own wording (issue/fix) must never reference another state (A-30). Evidence quotes are exempt."""
    for f in findings:
        if INTERSTATE_RX.search(f"{f.get('issue', '')} {f.get('fix', '')}") and not INTERSTATE_RX.search(f.get("evidence", "")):
            f["jurisdiction_check"] = "FAILED: interstate reference in TMP Check wording — reviewer must rewrite"
            f["original_severity"], f["severity"] = f.get("original_severity", f["severity"]), "Query"


def cost(u) -> float:
    return ((u.input_tokens or 0) * PRICE["input"] + (u.output_tokens or 0) * PRICE["output"]
            + (getattr(u, "cache_read_input_tokens", 0) or 0) * PRICE["cache_read"]
            + (getattr(u, "cache_creation_input_tokens", 0) or 0) * PRICE["cache_write"]) / 1e6


def run(pdf: Path, passes: list[str], dry_run: bool = False) -> dict:
    data = base64.standard_b64encode(pdf.read_bytes()).decode()
    doc = pymupdf.open(pdf)
    doc_block = {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data},
                 "title": pdf.name, "cache_control": {"type": "ephemeral"}}
    # Cloud sessions withhold ANTHROPIC_API_KEY, so TMPCHECK_ANTHROPIC_API_KEY is accepted too (Owner's PC uses the standard name)
    key = os.environ.get("TMPCHECK_ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=key or ("dry-run" if dry_run else None))
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
        for i, f in enumerate(res["findings"], 1):
            f["id"] = f"{code}-{i:03d}"
        validate(res["findings"], doc)
        jurisdiction_guard(res["findings"])
        u = msg.usage
        res["usage"] = {"input": u.input_tokens, "output": u.output_tokens,
                        "cache_read": getattr(u, "cache_read_input_tokens", 0),
                        "cache_write": getattr(u, "cache_creation_input_tokens", 0),
                        "usd": round(cost(u), 4), "seconds": round(time.time() - t0, 1), "stop_reason": msg.stop_reason}
        out["usd_total"] += res["usage"]["usd"]
        out["passes"][code] = res
        print(f"pass {code}: {len(res['findings'])} findings, ${res['usage']['usd']:.2f}, {res['usage']['seconds']}s, "
              f"cache read {res['usage']['cache_read']}")
    allf = [f for r in out["passes"].values() for f in r.get("findings", [])]
    out["findings"] = merge(allf)   # D4: one entry per distinct issue across passes
    out["merged_count"] = len(allf) - len(out["findings"])
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

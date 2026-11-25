"""Finding post-processing shared by the deterministic and LLM pipelines.

Fixes from the SU-series draft-report review (PROJECT_LOG 2026-11-25):
  D1  Evidence is verified with the SAME word-level locator the annotation step uses, so a finding
      is "verified" only if it can be boxed on the page. No box -> Query / Unable to verify.
  D2  VISUAL-only evidence cannot be machine-verified, so a VISUAL-only Critical is held as a Query
      (original severity kept for the reviewer). CLAUDE.md §2: no unsupported Critical is released.
  D3  Outcome label follows severity: Query -> "Unable to verify"; otherwise "Potential issue".
  D4  Duplicate findings (same issue raised by several passes / on several pages) are merged into
      one finding listing every page and source.
"""
from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

import pymupdf

SEV_RANK = {"Critical": 4, "Major": 3, "Moderate": 2, "Minor": 1, "Query": 0}
OUTCOME_QUERY, OUTCOME_ISSUE = "Unable to verify", "Potential issue"


def _tok(s: str) -> list[str]:
    # NFKC folds PDF ligatures ('ﬃ' -> 'ffi'), so 'traﬃc' on the page matches 'traffic' in a quote (check 14 review)
    return re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKC", s).lower())


def norm(s: str) -> str:
    return " ".join(_tok(s))


def is_visual(evidence: str) -> bool:
    return evidence.strip().upper().startswith("VISUAL:")


def locate(page: pymupdf.Page, evidence: str) -> list[list[float]] | None:
    """Word-level locator (same source as annotation): bboxes of the words forming `evidence`
    in reading order on `page`, or None if the token sequence is not on the page."""
    target = _tok(evidence)
    if not target:
        return None
    # one entry per token, each carrying its word's bbox (a word like "60km/h" yields 2 tokens)
    toks = [(t, w[:4]) for w in page.get_text("words", sort=True) for t in _tok(w[4])]
    n = len(target)
    for i in range(len(toks) - n + 1):
        if all(toks[i + k][0] == target[k] for k in range(n)):
            boxes = []
            for _, b in toks[i:i + n]:
                if not boxes or list(b) != boxes[-1]:
                    boxes.append([round(v, 1) for v in b])
            return boxes
    return None


def set_outcome(f: dict) -> dict:
    f["outcome"] = OUTCOME_QUERY if f.get("severity") == "Query" else OUTCOME_ISSUE
    return f


def hold_as_query(f: dict, reason: str) -> None:
    if f.get("severity") != "Query":
        f.setdefault("original_severity", f["severity"])
        f["severity"] = "Query"
    f["hold_reason"] = reason


VARIANT_SEP = re.compile(r"\s+(?:/|vs\.?|versus)\s+|\s*;\s*", re.I)


def locate_variants(doc: pymupdf.Document, evidence: str, first: int):
    """DEF-L06-1: style-variant evidence such as "car park / carpark / CarPark" lists forms
    found on different pages. Each variant must be located on some page (cited page first).
    Returns (page, boxes, {variant: page}) for the first variant, or None if any is missing."""
    parts = [v.strip(" '\"") for v in VARIANT_SEP.split(evidence) if v.strip(" '\"")]
    if len(parts) < 2:
        return None
    order = [first, *[i for i in range(1, len(doc) + 1) if i != first]]
    found = {}
    for v in parts:
        for p in order:
            if 1 <= p <= len(doc):
                boxes = locate(doc[p - 1], v)
                if boxes:
                    found[v] = (p, boxes)
                    break
        else:
            return None
    p0, b0 = found[parts[0]]
    return p0, b0, {v: pg for v, (pg, _) in found.items()}


def validate(findings: list[dict], doc: pymupdf.Document) -> list[dict]:
    """D1 + D2 + D3. Mutates and returns `findings`."""
    npages = len(doc)
    for f in findings:
        ev = f.get("evidence", "")
        if is_visual(ev):
            f["evidence_check"] = "visual — reviewer to confirm"
            if f.get("severity") == "Critical":
                hold_as_query(f, "VISUAL-only evidence cannot support a Critical finding")
            set_outcome(f)
            continue
        cands = [f["page"], *f.get("related_pages", []), f["page"] - 1, f["page"] + 1]
        hit = None
        for p in dict.fromkeys(cands):
            if 1 <= p <= npages:
                boxes = locate(doc[p - 1], ev)
                if boxes:
                    hit = (p, boxes)
                    break
        variants = None if hit else locate_variants(doc, ev, f["page"])
        if variants:
            hit = variants[:2]
            f["variant_pages"] = variants[2]
        if hit:
            if hit[0] != f["page"]:
                f.setdefault("page_as_cited", f["page"])
                f["page"] = hit[0]
            f["bbox"], f["evidence_check"] = hit[1], "verified"
        else:
            f["evidence_check"] = "NOT FOUND on cited page"
            hold_as_query(f, "Quoted evidence could not be located on the cited page")
        set_outcome(f)
    return findings


def _pages(f: dict) -> set[int]:
    return {f["page"], *f.get("related_pages", [])}


def _sim(a: str, b: str) -> float:
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:
        return 1.0 if min(len(a), len(b)) >= 15 else 0.0
    return SequenceMatcher(None, a, b).ratio()


def is_duplicate(a: dict, b: dict) -> bool:
    """Same issue if the issue text is near-identical and they share a page or the same evidence,
    or the evidence matches on a shared page and the issues are related. Rule-based findings use
    templated issue text, so two of them merge only on same rule + same evidence + shared page."""
    overlap = bool(_pages(a) & _pages(b))
    ev = 0.0 if is_visual(a.get("evidence", "")) else _sim(a.get("evidence", ""), b.get("evidence", ""))
    if a.get("rule") and b.get("rule"):
        return a["rule"] == b["rule"] and ev >= 0.9 and overlap
    issue = _sim(a.get("issue", ""), b.get("issue", ""))
    if issue >= 0.92 or (issue >= 0.85 and (overlap or ev >= 0.9)):  # e.g. same note on TGS 01 and 02
        return True
    return ev >= 0.9 and overlap and issue >= 0.5


def _key(f: dict):
    """Primary of a duplicate group: verified first, then highest severity."""
    return (f.get("evidence_check") == "verified", SEV_RANK.get(f.get("severity"), 0))


def merge(findings: list[dict]) -> list[dict]:
    """D4: merge duplicates. The primary keeps its text; others are listed in `merged_from`."""
    groups: list[list[dict]] = []
    for f in findings:
        g = next((g for g in groups if any(is_duplicate(f, x) for x in g)), None)
        (g.append(f) if g is not None else groups.append([f]))
    out = []
    for g in groups:
        g = sorted(g, key=_key, reverse=True)
        p = dict(g[0])
        if len(g) > 1:
            pages = sorted(set().union(*(_pages(x) for x in g)))
            p["related_pages"] = [x for x in pages if x != p["page"]]
            p["merged_from"] = [{k: x.get(k) for k in ("id", "pass", "rule", "page", "severity") if x.get(k) is not None}
                                for x in g[1:]]
        set_outcome(p)
        out.append(p)
    return out

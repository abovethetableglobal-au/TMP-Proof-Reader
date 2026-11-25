"""Score TMP Check findings against a reference ground-truth set (e.g. REF-01).

Matching = candidate proposal, not a verdict: a system finding is proposed against a reference
item when the pages overlap (±1) and the text overlaps; the best candidate wins and each reference
item is counted once. Unmatched findings are 'to adjudicate' (valid-not-in-reference or false
positive) — a person decides via the adjudication file. Overrides always beat auto-matching.

Reference file: {"items": [[id, category, [pages], "keywords"], ...]}  (empty pages = document-wide)
Adjudication file (optional): {"<source>:<finding id or index>": "<ref id>" | "FP" | "NEW" | "EXCLUDE"}

Usage: python -m src.tmpcheck.score <ref.json> <findings.json> [<findings.json> ...] [--adj adj.json] [--out score.json]
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

STOP = set("the a an of to and or in on is are be for with as by at no not this that from all vs has have".split())
CAT_NAMES = {"A": "Typos, grammar, style", "B": "Consistency", "C": "Template leftovers / completeness", "D": "TGS and figures"}


def toks(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOP and len(t) > 1}


def load_findings(path: Path) -> list[dict]:
    d = json.loads(path.read_text())
    src = path.stem
    if "passes" in d:   # llm_checks output
        out = []
        for code, p in d["passes"].items():
            for i, f in enumerate(p.get("findings", [])):
                out.append({**f, "key": f"{src}:{code}{i + 1:03d}"})
        return out
    return [{**f, "key": f"{src}:{f.get('id', i)}"} for i, f in enumerate(d["findings"])]   # det / template_diff


def similarity(f: dict, ref) -> float:
    rid, cat, pages, kw = ref
    fp = {f["page"], *f.get("related_pages", [])}
    if pages and not any(abs(a - b) <= 1 for a in fp for b in pages):
        return 0.0
    rt = toks(kw)
    ft = toks(" ".join(str(f.get(k, "")) for k in ("evidence", "issue", "fix", "section")))
    if not rt:
        return 0.0
    s = len(rt & ft) / len(rt)
    return s * (0.6 if not pages else 1.0)     # document-wide style items need stronger text evidence


def score(ref_items: list, findings: list[dict], adj: dict, threshold: float = 0.3) -> dict:
    by_id = {r[0]: r for r in ref_items}
    hit: dict[str, list[str]] = defaultdict(list)
    verdict = {}
    for f in findings:
        k = f["key"]
        if k in adj:
            v = adj[k]
            verdict[k] = v
            if v in by_id:
                hit[v].append(k)
            continue
        best = max(((similarity(f, r), r[0]) for r in ref_items), default=(0, None))
        if best[0] >= threshold:
            verdict[k] = best[1]
            hit[best[1]].append(k)
        else:
            verdict[k] = "UNMATCHED"
    cats = {}
    for c in CAT_NAMES:
        items = [r for r in ref_items if r[1] == c]
        cats[c] = {"name": CAT_NAMES[c], "reference": len(items), "found": sum(1 for r in items if hit.get(r[0]))}
    vc = Counter("match" if v in by_id else v for v in verdict.values())
    scored = vc["match"] + vc["NEW"] + vc["FP"]
    return {
        "recall": {"found": sum(c["found"] for c in cats.values()), "reference": len(ref_items), "by_category": cats},
        "findings": {"total": len(findings), **dict(vc)},
        "precision_scored": round((vc["match"] + vc["NEW"]) / scored, 3) if scored else None,
        "duplicates": {r: ks for r, ks in hit.items() if len(ks) > 1},
        "missed": [r[0] for r in ref_items if not hit.get(r[0])],
        "verdicts": verdict,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ref"); ap.add_argument("findings", nargs="+")
    ap.add_argument("--adj"); ap.add_argument("--out"); ap.add_argument("--threshold", type=float, default=0.3)
    a = ap.parse_args()
    ref = json.loads(Path(a.ref).read_text())["items"]
    fs = [f for p in a.findings for f in load_findings(Path(p))]
    adj = json.loads(Path(a.adj).read_text()) if a.adj else {}
    res = score(ref, fs, adj, a.threshold)
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=2))
    r = res["recall"]
    print(f"Recall {r['found']}/{r['reference']} ({r['found'] / r['reference']:.0%})")
    for c, v in r["by_category"].items():
        print(f"  {c} {v['name']:<36}{v['found']:>3}/{v['reference']}")
    print(f"Findings: {res['findings']}  precision (adjudicated+matched): {res['precision_scored']}")
    unmatched = [k for k, v in res["verdicts"].items() if v == "UNMATCHED"]
    if unmatched:
        print(f"To adjudicate ({len(unmatched)}): " + ", ".join(unmatched))

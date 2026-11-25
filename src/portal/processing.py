"""Upload intake and checking job (stage S4).

Flow: validate → store original (never modified) → run checks → findings saved →
status draft_review → 1 credit consumed (A-24). Any failure → status failed, no credit (A-05 rule 4).
AI passes run only when TMPCHECK_AI_PASSES is set (e.g. "A,B,C") and ANTHROPIC_API_KEY exists;
otherwise deterministic checks only. Approved AI use: A-16 / A-18 documents only.
"""
import json
import time
import os
import shutil
import subprocess
import tempfile
import re
import traceback
from difflib import SequenceMatcher
from pathlib import Path

from sqlalchemy.orm import Session

from .config import ROOT, settings
from .db import (Check, CheckStatus, CreditLedger, Finding, LedgerType, SessionLocal, utcnow)
from . import services

STORAGE = Path(os.environ.get("TMPCHECK_STORAGE", ROOT / "customer-docs" / "portal"))
SIGNATURES = {".pdf": b"%PDF-", ".docx": b"PK\x03\x04"}


def ai_status() -> tuple[str, str]:
    """('on'|'off'|'no_key', explanation) for the AI passes, read from this process's environment."""
    passes = os.environ.get("TMPCHECK_AI_PASSES", "").strip()
    if not passes:
        return "off", "AI passes are off (TMPCHECK_AI_PASSES not set in the window running the portal)."
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return "no_key", (f"AI passes {passes} were requested but no ANTHROPIC_API_KEY was found "
                          "in the window running the portal.")
    return "on", f"AI passes {passes} are on (×{ai_runs()} runs per check)."


def ai_runs() -> int:
    """How many times the AI passes run per check (results combined). Env TMPCHECK_AI_RUNS overrides config."""
    try:
        n = int(os.environ.get("TMPCHECK_AI_RUNS") or settings().get("ai", {}).get("runs", 1))
    except ValueError:
        n = 1
    return max(1, min(n, 3))


PASS_CATEGORY = {"A": "A Proofreading", "B": "B Consistency", "C": "C Completeness", "D": "D TGS cross-check"}
SEV_RANK = {"Critical": 0, "Major": 1, "Moderate": 2, "Minor": 3, "Query": 4}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", (s or "").lower())).strip()


def same_issue(a: dict, b: dict) -> bool:
    """Two findings describe the same issue: same page and overlapping evidence text."""
    if int(a.get("page") or 0) != int(b.get("page") or 0):
        return False
    ea, eb = _norm(a.get("evidence")), _norm(b.get("evidence"))
    if len(ea) < 12 or len(eb) < 12:
        return ea == eb and bool(ea)
    short, long_ = sorted((ea, eb), key=len)
    if short in long_ or long_.startswith(short[:60]):
        return True
    return SequenceMatcher(None, ea, eb).ratio() >= 0.75


def _sources(src: str, f: dict) -> set[str]:
    if "_sources" in f:
        return set(f["_sources"])
    if src == "deterministic":
        return {"rules"}
    if src == "ai":
        return {f"AI {f.get('pass', '')}".strip()}
    return {x.strip() for x in src.split(",") if x.strip()}


def _pages(f: dict) -> set[int]:
    return {int(f.get("page") or 1), *(int(p) for p in f.get("related_pages") or [])}


def _supported(f: dict) -> bool:
    """Evidence located on the page (AI findings carry evidence_check; rule findings are located by construction)."""
    return f.get("evidence_check", "verified") == "verified"


def merge(items: list[tuple[str, dict]]) -> tuple[str, dict]:
    """Merge findings that describe one problem. Severity and evidence come from members whose quote was located
    on the page; a merged finding with no located quote stays a Query (CLAUDE.md §2 — check 14/15 review: an
    unlocated quote was being carried as the evidence of a Major finding). Every page and source is kept."""
    if len(items) == 1 and "_sources" in items[0][1]:
        return items[0]
    fs = [f for _, f in items]
    backed = [f for f in fs if _supported(f)] or [f for f in fs if str(f.get("evidence", "")).upper().startswith("VISUAL:")]
    pool = backed or fs
    sev = min((f.get("severity", "Query") for f in pool), key=lambda s: SEV_RANK.get(s, 4)) if backed else "Query"
    if sev == "Critical" and not any(_supported(f) for f in pool):
        sev = "Query"                       # VISUAL-only Critical is held for the reviewer (postprocess D2)
    best = max(((s, f) for s, f in items if f in pool),
               key=lambda it: ("rules" not in _sources(*it), len(it[1].get("issue", ""))))[1]
    merged = dict(best, severity=sev)
    merged["evidence"] = max((f.get("evidence", "") for f in pool if _supported(f)), key=len, default=best.get("evidence", ""))
    merged["evidence_check"] = "verified" if any(_supported(f) for f in pool) else best.get("evidence_check")
    merged["outcome"] = "Unable to verify" if sev == "Query" else "Potential issue"
    held = [f.get("hold_reason") for f in fs if f.get("hold_reason")]
    merged["hold_reason"] = (held[0] if held else None) if sev == "Query" and not any(_supported(f) for f in fs) else None
    merged["rule"] = next((f.get("rule") for f in fs if f.get("rule")), None)
    pages = set().union(*(_pages(f) for f in fs))
    merged["page"] = min(int(f.get("page") or 1) for f in fs)
    merged["related_pages"] = sorted(pages - {merged["page"]})
    srcs = set().union(*(_sources(s, f) for s, f in items))
    merged["_sources"] = sorted(srcs)
    return ", ".join(sorted(srcs)), merged


def dedupe(results: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    """Step 1 (no AI): merge findings on the same page with overlapping evidence."""
    groups: list[list[tuple[str, dict]]] = []
    for item in results:
        for g in groups:
            if same_issue(g[0][1], item[1]):
                g.append(item)
                break
        else:
            groups.append([item])
    return [merge(g) for g in groups]


def style_rollup(items: list[tuple[str, dict]]) -> tuple[str, dict]:
    """Roll pure style/format consistency points into one finding, as a human proofreader's style list does."""
    src, base = merge(items)
    lines = [f"• p{f.get('page')}: {' '.join(str(f.get('issue', '')).split())}" for _, f in
             sorted(items, key=lambda it: int(it[1].get("page") or 1))]
    base.update(severity="Minor", category="A Proofreading", outcome="Potential issue", rule=None,
                issue=f"Style inconsistencies to standardise across the document ({len(items)} items). "
                      "Choose one form for each item and apply it throughout.",
                evidence="\n".join(lines), action="Standardise each item listed.")
    return src, base


def consolidate(results: list[tuple[str, dict]], grouper) -> list[tuple[str, dict]]:
    """Step 2 (AI): group findings that describe the same problem across pages/passes; roll up style points.
    `grouper(findings) -> [(indices, kind)]`. Any failure leaves the findings as they were."""
    if len(results) < 2:
        return results
    groups = grouper([f for _, f in results])
    out, style = [], []
    for idx, kind in groups:
        merged = merge([results[i] for i in idx])
        (style if kind == "style_variant" else out).append(merged)
    if len(style) > 1:
        out.append(style_rollup(style))
    else:
        out += style
    return out


class UploadError(ValueError):
    """Customer-facing rejection message. No credit is used."""


def validate_upload(filename: str, data: bytes) -> str:
    up = settings()["upload"]
    ext = Path(filename).suffix.lower()
    if ext not in up["allowed_extensions"]:
        raise UploadError("This file type is not supported. Upload a PDF or Word (.docx) file.")
    if not data:
        raise UploadError("This file is empty.")
    if len(data) > up["max_bytes"]:
        raise UploadError(f"This file is {len(data) / 1048576:.1f} MB. The maximum size is "
                          f"{up['max_bytes'] / 1048576:.0f} MB.")
    if not data.startswith(SIGNATURES[ext]):
        raise UploadError(f"This file does not appear to be a valid {ext[1:].upper()} document. "
                          "It may be damaged or renamed.")
    return ext


def safe_doc_ref(filename: str) -> str:
    stem = Path(filename).stem
    return "".join(ch for ch in stem if ch.isalnum() or ch in "-_ .")[:120].strip() or "Untitled"


def create_check(db: Session, org_id: int, filename: str, data: bytes) -> Check:
    ext = validate_upload(filename, data)
    if services.credit_balance(db, org_id).available < 1:
        raise UploadError("You have no credits available. Request credits on the Credits & Billing page.")
    chk = Check(org_id=org_id, doc_ref=safe_doc_ref(filename), filename=Path(filename).name[:300],
                status=CheckStatus.uploaded)
    db.add(chk)
    db.flush()
    folder = STORAGE / str(org_id) / str(chk.id)
    folder.mkdir(parents=True, exist_ok=True)
    original = folder / f"original{ext}"
    original.write_bytes(data)
    chk.storage_path = str(original)
    db.commit()
    return chk


def to_pdf(original: Path) -> Path:
    if original.suffix == ".pdf":
        return original
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise UploadError("Word documents can't be converted on this computer (LibreOffice not installed). "
                          "Save the TMP as PDF and upload again.")
    out = original.parent
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out), str(original)],
                   check=True, capture_output=True, timeout=180)
    pdf = out / (original.stem + ".pdf")
    if not pdf.exists():
        raise UploadError("The Word document could not be converted. Save it as PDF and upload again.")
    return pdf


def _consume_credit(db: Session, chk: Check) -> None:
    """A-24: one credit on delivery of the draft to the reviewer; oldest-expiring lot first."""
    now = utcnow()
    rows = db.query(CreditLedger).filter_by(org_id=chk.org_id).all()
    remaining, expiry = {}, {}
    for r in rows:
        lot = r.lot_id or r.id
        remaining[lot] = remaining.get(lot, 0) + r.qty
        if r.type == LedgerType.purchase:
            expiry[lot] = services._aware(r.expires_at)
    usable = [lot for lot, q in remaining.items() if q > 0 and lot in expiry and expiry[lot] > now]
    if not usable:
        raise RuntimeError("No credit available at draft delivery")
    lot = min(usable, key=lambda x: expiry[x])
    db.add(CreditLedger(org_id=chk.org_id, lot_id=lot, type=LedgerType.consume, qty=-1, check_id=chk.id,
                        created_by="system", reason="Draft delivered to reviewer (A-24)"))


session_factory = SessionLocal   # replaced in tests


def recover_interrupted() -> int:
    """At startup: a check still 'processing' was cut off when the portal stopped (nothing is running any more).
    Mark it failed — no credit is consumed (A-05 rule 4) — so it does not sit at 'Processing' for ever."""
    db = session_factory()
    try:
        stuck = db.query(Check).filter(Check.status == CheckStatus.processing).all()
        for chk in stuck:
            chk.status = CheckStatus.failed
            chk.failure_reason = "Processing was interrupted because the portal was stopped. No credit was used. Please upload again."
        db.commit()
        return len(stuck)
    finally:
        db.close()


class Timer:
    """Records how long each processing stage takes; stored on the check as JSON (Owner request 2026-11-25)."""
    def __init__(self):
        self.t0 = self.last = time.monotonic()
        self.stages: list[list] = []

    def lap(self, stage: str) -> None:
        now = time.monotonic()
        self.stages.append([stage, round(now - self.last, 1)])
        self.last = now

    def add(self, stage: str, seconds: float) -> None:
        self.stages.append([stage, round(float(seconds), 1)])

    def total(self) -> float:
        return round(time.monotonic() - self.t0, 1)


def _finish_timing(chk: Check, timer: Timer) -> None:
    chk.processing_finished_at = utcnow()
    chk.processing_seconds = timer.total()
    chk.timings = json.dumps(timer.stages)
    print(f"TMP Check portal: check {chk.id} ({chk.doc_ref}) {chk.status.value} in {fmt_duration(chk.processing_seconds)}",
          flush=True)


def fmt_duration(seconds: float | None) -> str:
    if seconds is None:
        return "—"
    m, s = divmod(int(round(seconds)), 60)
    h, m = divmod(m, 60)
    return f"{h} h {m} min" if h else f"{m} min {s} s" if m else f"{s} s"


def run_check(check_id: int) -> None:
    db = session_factory()
    timer = Timer()
    try:
        chk = db.get(Check, check_id)
        chk.status = CheckStatus.processing
        chk.processing_started_at = utcnow()
        db.commit()
        try:
            pdf = to_pdf(Path(chk.storage_path))
            import pymupdf
            with pymupdf.open(pdf) as doc:
                n = doc.page_count
            limit = settings()["upload"]["max_total_pages"]
            if n > limit:   # A-26
                raise UploadError(f"This package has {n} pages. The limit is {limit} pages including drawings.")
            if not any(p.get_text().strip() for p in pymupdf.open(pdf)):
                raise UploadError("No readable text was found (scanned document). Scanned TMPs are not yet supported.")
            chk.pages = n
            timer.lap("Convert and validate")

            from src.tmpcheck import det_checks
            results = [("deterministic", f) for f in det_checks.run(pdf)["findings"]]
            timer.lap("Rule checks")

            passes = os.environ.get("TMPCHECK_AI_PASSES", "").strip()
            state, why = ai_status()
            chk.ai_passes = None if state == "on" else f"skipped: {why}"
            if state == "on":
                from src.tmpcheck import llm_checks
                runs = ai_runs()
                total = 0.0
                for r in range(1, runs + 1):   # BENCH-04: repeat runs and combine (grouping removes the overlap)
                    ai = llm_checks.run(pdf, passes.split(","))
                    total += ai["usd_total"]
                    for code, p in ai["passes"].items():
                        if "usage" in p:
                            timer.add(f"AI run {r} pass {code}", p["usage"]["seconds"])
                    timer.lap(f"AI run {r} (total)")
                    for p in ai["passes"].values():
                        for f in p.get("findings", []):
                            f.setdefault("category", PASS_CATEGORY.get(f.get("pass"), ""))
                            results.append(("ai", f))
                chk.ai_passes = passes + (f" ×{runs}" if runs > 1 else "")
                chk.ai_cost_usd = f"{total:.2f}"

            merged = dedupe(results)
            timer.lap("Merge duplicates")
            if state == "on":
                try:
                    from src.tmpcheck import consolidate as cons
                    usd = [0.0]

                    def grouper(fs):
                        groups, cost = cons.group_findings(fs)
                        usd[0] = cost
                        return groups
                    merged = consolidate(merged, grouper)
                    chk.ai_cost_usd = f"{float(chk.ai_cost_usd or 0) + usd[0]:.2f}"
                except Exception:   # consolidation is an aid; never fail the check over it
                    traceback.print_exc()
                timer.lap("AI grouping")
            for src, f in merged:
                db.add(Finding(check_id=chk.id, severity=f.get("severity", "Query"), page=int(f.get("page") or 1),
                               section=str(f.get("section") or f.get("category") or "")[:200],
                               evidence=f.get("evidence", ""), issue=f.get("issue", ""),
                               action=f.get("action") or f.get("fix") or f.get("suggested_correction"),
                               category=f.get("category", ""), outcome=f.get("outcome", "Potential issue"),
                               rule=f.get("rule") or f.get("rule_id"), source=src, hold_reason=f.get("hold_reason"),
                               pages=", ".join(map(str, sorted(_pages(f)))) if f.get("related_pages") else None))
            _consume_credit(db, chk)
            chk.status = CheckStatus.draft_review
            timer.lap("Save findings")
            _finish_timing(chk, timer)
            db.commit()
        except Exception as e:  # any failure: no credit (A-05 rule 4)
            db.rollback()
            chk = db.get(Check, check_id)
            chk.status = CheckStatus.failed
            chk.failure_reason = str(e) if isinstance(e, UploadError) else \
                "Processing failed. No credit was used. Please try again or contact support."
            timer.lap("Failed")
            _finish_timing(chk, timer)
            db.commit()
            if not isinstance(e, UploadError):
                traceback.print_exc()
    finally:
        db.close()


def disposition(db: Session, f: Finding, decision: str, note: str | None) -> None:
    if decision not in ("accepted", "edited", "rejected", "pending"):
        raise ValueError("Invalid decision")
    if decision == "edited" and not (note or "").strip():
        raise UploadError("Add a note describing the edit.")
    f.disposition = decision
    f.reviewer_note = (note or "").strip() or None
    f.dispositioned_at = utcnow() if decision != "pending" else None


def compliance_sources() -> list[dict]:
    """Sources of the approved rules in the compliance library, for the report (Handover §6)."""
    import yaml
    from .config import RULES_DIR
    out: dict[tuple, int] = {}
    for p in sorted(RULES_DIR.glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        r = yaml.safe_load(p.read_text(encoding="utf-8"))
        if r.get("status") == "approved":
            k = (r.get("source_name", ""), str(r.get("edition", "")), r.get("authority", ""))
            out[k] = out.get(k, 0) + 1
    return [{"name": n, "edition": e, "authority": a, "count": c} for (n, e, a), c in out.items()]


def finding_rows(db: Session, chk: Check) -> list[dict]:
    return [{"id": f.id, "page": f.page, "pages": f.pages, "severity": f.severity, "category": f.category,
             "issue": f.issue, "evidence": f.evidence, "action": f.action, "outcome": f.outcome, "rule": f.rule,
             "source": f.source, "hold_reason": f.hold_reason, "disposition": f.disposition, "reviewer_note": f.reviewer_note}
            for f in db.query(Finding).filter_by(check_id=chk.id).all()]


def build_outputs(db: Session, chk: Check, folder: Path, final: bool) -> tuple[Path, Path]:
    """Output 1 (report PDF) and Output 2 (annotated copy) — same F-numbers in both."""
    from src.tmpcheck import outputs
    org = chk_org_name(db, chk)
    rows = finding_rows(db, chk)
    items = outputs.number_findings(rows, final)
    meta = outputs.Meta(doc_ref=chk.doc_ref, filename=chk.filename, organisation=org, pages=chk.pages,
                        uploaded=chk.created_at, final=final, reviewer=chk.reviewer_name or "",
                        final_date=chk.final_issued_at, ai_passes=(chk.ai_passes or "") if not
                        (chk.ai_passes or "").startswith("skipped") else "", sources=compliance_sources())
    folder.mkdir(parents=True, exist_ok=True)
    kind = "final" if final else "draft"
    annotated = outputs.annotate(to_pdf(Path(chk.storage_path)), items, folder / f"{kind}-annotated.pdf", final)
    report = outputs.build_report(meta, items, rows, folder / f"{kind}-report.pdf")
    return report, annotated


def chk_org_name(db: Session, chk: Check) -> str:
    from .db import Organisation
    org = db.get(Organisation, chk.org_id)
    return org.name if org else ""


def final_paths(chk: Check) -> tuple[Path, Path]:
    folder = Path(chk.storage_path).parent
    return folder / "final-report.pdf", folder / "final-annotated.pdf"


def issue_final(db: Session, chk: Check, reviewer: str = "") -> None:
    """A-15: final only after every finding has been dispositioned by the reviewer.
    The final report and annotated copy are produced and stored at issue, so they never change afterwards."""
    if chk.status != CheckStatus.draft_review:
        raise UploadError("Only a draft can be issued as final.")
    pending = db.query(Finding).filter_by(check_id=chk.id, disposition="pending").count()
    if pending:
        raise UploadError(f"{pending} finding(s) still need a decision before the final can be issued.")
    chk.reviewer_name = reviewer or chk.reviewer_name
    chk.final_issued_at = utcnow()
    try:
        build_outputs(db, chk, Path(chk.storage_path).parent, final=True)
    except Exception as e:
        traceback.print_exc()
        chk.final_issued_at = None
        raise UploadError("The final report could not be produced. The check is still a draft; please try again.") from e
    chk.status = CheckStatus.final_issued

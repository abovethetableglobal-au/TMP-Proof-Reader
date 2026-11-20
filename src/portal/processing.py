"""Upload intake and checking job (stage S4).

Flow: validate → store original (never modified) → run checks → findings saved →
status draft_review → 1 credit consumed (A-24). Any failure → status failed, no credit (A-05 rule 4).
AI passes run only when TMPCHECK_AI_PASSES is set (e.g. "A,B,C") and ANTHROPIC_API_KEY exists;
otherwise deterministic checks only. Approved AI use: A-16 / A-18 documents only.
"""
import os
import shutil
import subprocess
import tempfile
import traceback
from pathlib import Path

from sqlalchemy.orm import Session

from .config import ROOT, settings
from .db import (Check, CheckStatus, CreditLedger, Finding, LedgerType, SessionLocal, utcnow)
from . import services

STORAGE = Path(os.environ.get("TMPCHECK_STORAGE", ROOT / "customer-docs" / "portal"))
SIGNATURES = {".pdf": b"%PDF-", ".docx": b"PK\x03\x04"}


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


def run_check(check_id: int) -> None:
    db = session_factory()
    try:
        chk = db.get(Check, check_id)
        chk.status = CheckStatus.processing
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

            from src.tmpcheck import det_checks
            results = [("deterministic", f) for f in det_checks.run(pdf)["findings"]]

            passes = os.environ.get("TMPCHECK_AI_PASSES", "").strip()
            if passes and os.environ.get("ANTHROPIC_API_KEY"):
                from src.tmpcheck import llm_checks
                ai = llm_checks.run(pdf, passes.split(","))
                for p in ai["passes"].values():
                    results += [("ai", f) for f in p.get("findings", [])]
                chk.ai_passes = passes
                chk.ai_cost_usd = f"{ai['usd_total']:.2f}"

            for src, f in results:
                db.add(Finding(check_id=chk.id, severity=f.get("severity", "Query"), page=int(f.get("page") or 1),
                               section=str(f.get("section") or f.get("category") or "")[:200],
                               evidence=f.get("evidence", ""), issue=f.get("issue", ""),
                               action=f.get("action") or f.get("suggested_correction"),
                               category=f.get("category", ""), outcome=f.get("outcome", "Potential issue"),
                               rule=f.get("rule") or f.get("rule_id"), source=src))
            _consume_credit(db, chk)
            chk.status = CheckStatus.draft_review
            db.commit()
        except Exception as e:  # any failure: no credit (A-05 rule 4)
            db.rollback()
            chk = db.get(Check, check_id)
            chk.status = CheckStatus.failed
            chk.failure_reason = str(e) if isinstance(e, UploadError) else \
                "Processing failed. No credit was used. Please try again or contact support."
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


def issue_final(db: Session, chk: Check) -> None:
    """A-15: final only after every finding has been dispositioned by the reviewer."""
    if chk.status != CheckStatus.draft_review:
        raise UploadError("Only a draft can be issued as final.")
    pending = db.query(Finding).filter_by(check_id=chk.id, disposition="pending").count()
    if pending:
        raise UploadError(f"{pending} finding(s) still need a decision before the final can be issued.")
    chk.status = CheckStatus.final_issued
    chk.final_issued_at = utcnow()

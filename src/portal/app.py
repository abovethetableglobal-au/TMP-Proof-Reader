"""TMP Check customer portal — FastAPI + Jinja2 (A-21, local build).

Run:  uvicorn src.portal.app:app --reload
Stage S1: shell, navigation, live-data dashboard with empty states.
Authentication arrives in S2; until then a local dev context is used and the
app refuses to start unless TMPCHECK_ENV=local.
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

import yaml
from fastapi import BackgroundTasks, Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import processing, services
from .config import RULES_DIR, money, price_label, settings
from .db import Check, CheckStatus, Finding, Organisation, SessionLocal, User, init_db

HERE = Path(__file__).parent


@asynccontextmanager
async def lifespan(_app):
    if os.environ.get("TMPCHECK_ENV") != "local":
        raise RuntimeError("Portal has no authentication yet (stage S2). Set TMPCHECK_ENV=local to run locally.")
    init_db()
    print("TMP Check portal:", processing.ai_status()[1], flush=True)
    yield


app = FastAPI(title="TMP Check", docs_url=None, redoc_url=None, lifespan=lifespan)

app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
templates = Jinja2Templates(directory=HERE / "templates")
templates.env.globals.update(money=money, price_label=price_label, cfg=settings)
# Portable date format (strftime "%-d" is not supported on Windows)
templates.env.filters["dmy"] = lambda d: f"{d.day} {d:%b %Y}" if d else ""

NAV = [
    ("dashboard", "Dashboard", "/", "home"),
    ("new_check", "New Check", "/checks/new", "upload"),
    ("my_checks", "My Checks", "/checks", "doc"),
    ("billing", "Credits & Billing", "/billing", "card"),
    ("library", "Compliance Library", "/library", "book"),
    ("help", "Help & Support", "/help", "help"),
]
templates.env.globals["NAV"] = NAV




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Ctx:
    def __init__(self, user: User, org: Organisation):
        self.user, self.org = user, org


def current(db: Session = Depends(get_db)) -> Ctx:
    """S1 placeholder for authentication: the local dev user (TMPCHECK_DEV_USER, default id 1).
    Replaced by session login in S2."""
    uid = int(os.environ.get("TMPCHECK_DEV_USER", "1"))
    user = db.get(User, uid)
    if user is None:
        raise HTTPException(503, "No local user. Run: python -m src.portal.devseed")
    return Ctx(user, db.get(Organisation, user.org_id))


def render(request: Request, name: str, active: str, ctx: Ctx, **kw) -> HTMLResponse:
    return templates.TemplateResponse(request, name, {"active": active, "ctx": ctx, **kw})


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    return render(request, "pages/dashboard.html", "dashboard", ctx, d=services.dashboard(db, ctx.org))


@app.get("/checks/new", response_class=HTMLResponse)
def new_check(request: Request, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    return render(request, "pages/new_check.html", "new_check", ctx,
                  credits=services.credit_balance(db, ctx.org.id))


@app.get("/checks", response_class=HTMLResponse)
def my_checks(request: Request, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    return render(request, "pages/my_checks.html", "my_checks", ctx,
                  rows=services.recent_checks(db, ctx.org.id, limit=200))


@app.get("/billing", response_class=HTMLResponse)
def billing(request: Request, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    products = [p for p in settings()["credit_products"] if p["offered"]]
    return render(request, "pages/billing.html", "billing", ctx,
                  credits=services.credit_balance(db, ctx.org.id), products=products,
                  history=services.ledger_history(db, ctx.org.id))


def load_rules() -> list[dict]:
    rules = []
    for p in sorted(RULES_DIR.glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        r = yaml.safe_load(p.read_text(encoding="utf-8"))
        if r.get("status") == "approved":
            rules.append(r)
    return rules


@app.get("/library", response_class=HTMLResponse)
def library(request: Request, ctx: Ctx = Depends(current)):
    return render(request, "pages/library.html", "library", ctx, rules=load_rules())


@app.get("/help", response_class=HTMLResponse)
def help_page(request: Request, ctx: Ctx = Depends(current)):
    return render(request, "pages/help.html", "help", ctx)


# ---------- S4/S5: upload, check detail, reviewer workflow ----------

def get_check(db: Session, ctx: Ctx, check_id: int) -> Check:
    """Tenant-scoped lookup: another organisation's check is indistinguishable from a missing one."""
    chk = db.get(Check, check_id)
    if chk is None or chk.org_id != ctx.org.id:
        raise HTTPException(404, "Check not found")
    return chk


@app.post("/checks/upload")
async def upload(background: BackgroundTasks, file: UploadFile = File(...),
                 ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    data = await file.read(settings()["upload"]["max_bytes"] + 1)
    try:
        chk = processing.create_check(db, ctx.org.id, file.filename or "upload", data)
    except processing.UploadError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    background.add_task(processing.run_check, chk.id)
    return {"id": chk.id, "url": f"/checks/{chk.id}"}


@app.get("/checks/{check_id}", response_class=HTMLResponse)
def check_detail(check_id: int, request: Request, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    chk = get_check(db, ctx, check_id)
    order = {s: i for i, s in enumerate(services.SEVERITIES)}
    findings = sorted(db.query(Finding).filter_by(check_id=chk.id).all(),
                      key=lambda f: (order.get(f.severity, 9), f.page, f.id))
    label, tone = services.STATUS_LABELS[chk.status]
    pending = sum(1 for f in findings if f.disposition == "pending")
    counts = {s: sum(1 for f in findings if f.severity == s) for s in services.SEVERITIES}
    return render(request, "pages/check_detail.html", "my_checks", ctx, chk=chk, findings=findings,
                  status_label=label, tone=tone, pending=pending, counts=counts,
                  error=request.query_params.get("error"), CheckStatus=CheckStatus,
                  ai_now=processing.ai_status())


@app.get("/checks/{check_id}/status")
def check_status(check_id: int, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    return {"status": get_check(db, ctx, check_id).status.value}


@app.post("/checks/{check_id}/findings/{finding_id}")
def decide(check_id: int, finding_id: int, decision: str = Form(...), note: str = Form(""),
           ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    chk = get_check(db, ctx, check_id)
    f = db.get(Finding, finding_id)
    if f is None or f.check_id != chk.id:
        raise HTTPException(404, "Finding not found")
    if chk.status != CheckStatus.draft_review:
        raise HTTPException(409, "Findings can only be changed while the report is a draft")
    try:
        processing.disposition(db, f, decision, note)
    except processing.UploadError as e:
        return RedirectResponse(f"/checks/{chk.id}?error={e}#f{f.id}", status_code=303)
    db.commit()
    return RedirectResponse(f"/checks/{chk.id}#f{f.id}", status_code=303)


@app.post("/checks/{check_id}/final")
def final(check_id: int, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    chk = get_check(db, ctx, check_id)
    try:
        processing.issue_final(db, chk, reviewer=ctx.user.name)
    except processing.UploadError as e:
        return RedirectResponse(f"/checks/{chk.id}?error={e}", status_code=303)
    db.commit()
    return RedirectResponse(f"/checks/{chk.id}", status_code=303)


@app.get("/checks/{check_id}/findings.json")
def export_findings(check_id: int, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    """Findings with reviewer decisions — used for benchmarking (TEST_METHODOLOGY)."""
    chk = get_check(db, ctx, check_id)
    rows = db.query(Finding).filter_by(check_id=chk.id).order_by(Finding.page, Finding.id).all()
    return JSONResponse({"check_id": chk.id, "doc_ref": chk.doc_ref, "pages": chk.pages, "ai_passes": chk.ai_passes,
                         "ai_cost_usd": chk.ai_cost_usd, "status": chk.status.value,
                         "findings": [{"id": f.id, "page": f.page, "pages": f.pages, "severity": f.severity, "category": f.category,
                                       "rule": f.rule, "source": f.source, "issue": f.issue, "evidence": f.evidence,
                                       "action": f.action, "disposition": f.disposition,
                                       "reviewer_note": f.reviewer_note} for f in rows]},
                        headers={"Content-Disposition": f'attachment; filename="check-{chk.id}-findings.json"'})


def _output(db: Session, ctx: Ctx, check_id: int, which: int) -> Response:
    chk = get_check(db, ctx, check_id)
    names = ("report", "annotated")
    label = f"{chk.doc_ref} - TMP Check {'report' if which == 0 else 'annotated'}"
    if chk.status == CheckStatus.final_issued:
        path = processing.final_paths(chk)[which]
        if not path.exists():
            raise HTTPException(404, "Final file not found")
        return FileResponse(path, filename=f"{label} (final).pdf", media_type="application/pdf")
    if chk.status != CheckStatus.draft_review:
        raise HTTPException(409, "No report until the check has finished")
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        paths = processing.build_outputs(db, chk, Path(tmp), final=False)
        data = paths[which].read_bytes()
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{label} (DRAFT).pdf"'})


@app.get("/checks/{check_id}/report.pdf")
def report_pdf(check_id: int, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    return _output(db, ctx, check_id, 0)


@app.get("/checks/{check_id}/annotated.pdf")
def annotated_pdf(check_id: int, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    return _output(db, ctx, check_id, 1)


@app.get("/checks/{check_id}/original")
def original(check_id: int, ctx: Ctx = Depends(current), db: Session = Depends(get_db)):
    chk = get_check(db, ctx, check_id)
    if not chk.storage_path:
        raise HTTPException(404)
    return FileResponse(chk.storage_path, filename=chk.filename)

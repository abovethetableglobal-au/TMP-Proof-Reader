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
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import services
from .config import RULES_DIR, money, price_label, settings
from .db import Organisation, SessionLocal, User, init_db

HERE = Path(__file__).parent


@asynccontextmanager
async def lifespan(_app):
    if os.environ.get("TMPCHECK_ENV") != "local":
        raise RuntimeError("Portal has no authentication yet (stage S2). Set TMPCHECK_ENV=local to run locally.")
    init_db()
    yield


app = FastAPI(title="TMP Check", docs_url=None, redoc_url=None, lifespan=lifespan)

app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
templates = Jinja2Templates(directory=HERE / "templates")
templates.env.globals.update(money=money, price_label=price_label, cfg=settings)

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
                  credits=services.credit_balance(db, ctx.org.id), products=products)


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

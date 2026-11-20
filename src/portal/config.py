"""Load portal configuration (prices, tax, upload limits, branding)."""
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "portal.yaml"
RULES_DIR = ROOT / "compliance" / "rules"


@lru_cache
def settings() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    if cfg["tax"]["gst_registered"] and cfg["tax"]["price_display"] not in ("incl", "excl"):
        raise ValueError("tax.price_display must be 'incl' or 'excl'")
    return cfg


def money(amount: float) -> str:
    """Format an AUD amount, e.g. 1341 -> '$1,341.00'."""
    return f"${amount:,.2f}"


def price_label() -> str:
    """Tax wording for price displays. Never claims GST-inclusive while unregistered (A-04)."""
    tax = settings()["tax"]
    if not tax["gst_registered"]:
        return "AUD. GST not charged."
    return "AUD incl. GST" if tax["price_display"] == "incl" else "AUD excl. GST"

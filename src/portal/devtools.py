"""Local test helpers — change the dev account so each dashboard state can be tried.

Writes only to the local dev database (refuses unless TMPCHECK_ENV=local).
Data created here is test data, never shown as real customer information.

    python -m src.portal.devtools sub active|none|lapsed|cancelled
    python -m src.portal.devtools credits 10 [--days-ago 0]
    python -m src.portal.devtools use-credit
    python -m src.portal.devtools check REF-001 draft_review|final_issued|processing|failed [--findings Critical=1,Major=2]
    python -m src.portal.devtools reset
"""
import argparse
import os
import sys
from datetime import timedelta

from .db import (Check, CheckStatus, CreditLedger, Finding, LedgerType, Organisation,
                 SessionLocal, SubscriptionStatus, init_db, utcnow)


def main() -> None:
    if os.environ.get("TMPCHECK_ENV") != "local":
        sys.exit("Refusing: set TMPCHECK_ENV=local (local test database only).")
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("sub"); s.add_argument("status", choices=[x.value for x in SubscriptionStatus])
    c = sp.add_parser("credits"); c.add_argument("qty", type=int); c.add_argument("--days-ago", type=int, default=0)
    sp.add_parser("use-credit")
    k = sp.add_parser("check"); k.add_argument("ref"); k.add_argument("status", choices=[x.value for x in CheckStatus])
    k.add_argument("--findings", default="", help="e.g. Critical=1,Major=2,Minor=3")
    sp.add_parser("reset")
    a = ap.parse_args()

    init_db()
    with SessionLocal() as db:
        org = db.query(Organisation).first()
        if org is None:
            sys.exit("No dev organisation. Run: python -m src.portal.devseed")
        now = utcnow()
        if a.cmd == "sub":
            org.subscription_status = SubscriptionStatus(a.status)
        elif a.cmd == "credits":
            when = now - timedelta(days=a.days_ago)
            r = CreditLedger(org_id=org.id, type=LedgerType.purchase, qty=a.qty, created_at=when,
                             expires_at=when + timedelta(days=365), created_by="devtools",
                             payment_ref="TEST", reason="Local test data")
            db.add(r); db.flush(); r.lot_id = r.id
        elif a.cmd == "use-credit":
            lot = (db.query(CreditLedger).filter_by(org_id=org.id, type=LedgerType.purchase)
                   .filter(CreditLedger.expires_at > now).order_by(CreditLedger.expires_at).first())
            if lot is None:
                sys.exit("No unexpired credits to use.")
            db.add(CreditLedger(org_id=org.id, lot_id=lot.id, type=LedgerType.consume, qty=-1,
                                created_by="devtools", reason="Local test data"))
        elif a.cmd == "check":
            st = CheckStatus(a.status)
            chk = Check(org_id=org.id, doc_ref=a.ref, filename=f"{a.ref}.pdf", status=st,
                        final_issued_at=now if st == CheckStatus.final_issued else None,
                        failure_reason="Test failure" if st == CheckStatus.failed else None)
            db.add(chk); db.flush()
            for part in filter(None, a.findings.split(",")):
                sev, n = part.split("=")
                for i in range(int(n)):
                    db.add(Finding(check_id=chk.id, severity=sev.strip(), page=1, section="Test",
                                   evidence="Local test data"))
        elif a.cmd == "reset":
            db.query(Finding).delete(); db.query(Check).delete(); db.query(CreditLedger).delete()
            org.subscription_status = SubscriptionStatus.none
        db.commit()
    print("Done. Refresh the browser.")


if __name__ == "__main__":
    main()

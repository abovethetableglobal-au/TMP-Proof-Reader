"""Create the local development organisation and user.

No credits, checks or savings baseline are seeded: the dashboard must show
genuine empty states, never mock-up figures (brief §4).

    python -m src.portal.devseed [--org "Name"] [--user "Name"] [--email x@y]
"""
import argparse

from .db import Organisation, SessionLocal, User, init_db


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", default="Development Organisation")
    ap.add_argument("--user", default="Local Developer")
    ap.add_argument("--email", default="dev@localhost")
    a = ap.parse_args()
    init_db()
    with SessionLocal() as db:
        if db.query(User).filter_by(email=a.email).first():
            print("Dev user already exists.")
            return
        org = Organisation(name=a.org)
        db.add(org)
        db.flush()
        db.add(User(org_id=org.id, name=a.user, email=a.email, role="customer_user"))
        db.commit()
        print(f"Created org {org.id} '{a.org}' and user '{a.user}'.")


if __name__ == "__main__":
    main()

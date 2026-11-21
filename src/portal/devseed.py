"""Create or update a local organisation user with a password and role.

No credits or checks are seeded: the dashboard must show genuine empty states, never mock-up
figures (brief §4). Local build only (A-21).

    python -m src.portal.devseed --org "Name" --user "Name" --email you@example.com --role customer_reviewer
    (you are prompted for the password; or pass --password)

Roles: customer_user (upload, view) · customer_reviewer (also decides findings, issues finals) · admin
Running it again for an existing email updates the name, role and password.
"""
import argparse
import getpass

from .auth import hash_password
from .db import Organisation, SessionLocal, User, init_db

ROLES = ("customer_user", "customer_reviewer", "admin")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", default="Development Organisation")
    ap.add_argument("--user", default="Local Developer")
    ap.add_argument("--email", default="dev@localhost")
    ap.add_argument("--role", choices=ROLES, default="customer_reviewer")
    ap.add_argument("--password", help="at least 10 characters; prompted for if omitted")
    a = ap.parse_args()
    pw = a.password or getpass.getpass("Password (10+ characters): ")
    pw_hash = hash_password(pw)
    email = a.email.strip().lower()
    init_db()
    with SessionLocal() as db:
        user = db.query(User).filter_by(email=email).first()
        if user:
            user.name, user.role, user.password_hash = a.user, a.role, pw_hash
            db.commit()
            print(f"Updated user {email} ({a.role}).")
            return
        org = db.query(Organisation).filter_by(name=a.org).first()
        if org is None:
            org = Organisation(name=a.org)
            db.add(org)
            db.flush()
        db.add(User(org_id=org.id, name=a.user, email=email, role=a.role, password_hash=pw_hash))
        db.commit()
        print(f"Created user {email} ({a.role}) in '{org.name}'. Sign in at http://localhost:8000/login")


if __name__ == "__main__":
    main()

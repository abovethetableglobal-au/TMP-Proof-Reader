"""Sign-in, sessions, CSRF and audit logging (stage S2). Standard library only.

- Passwords: scrypt with a per-user salt.
- Sessions: random token in an HttpOnly, SameSite=Lax cookie; only its SHA-256 is stored server-side.
- CSRF: every POST must carry a token derived from the session (form field or X-CSRF-Token header).
- Roles: customer_user (upload, view), customer_reviewer (also decides findings and issues finals), admin.
"""
import hashlib
import hmac
import os
import secrets
import time
from datetime import timedelta

from sqlalchemy.orm import Session

from .config import ROOT
from .db import AuditEvent, User, UserSession, utcnow

COOKIE = "tmpcheck_session"
SESSION_HOURS = 12
REVIEWER_ROLES = {"customer_reviewer", "admin"}
_SCRYPT = dict(n=2 ** 14, r=8, p=1, dklen=32)
_failures: dict[str, list[float]] = {}        # email -> recent failure times (simple lockout)
LOCK_AFTER, LOCK_SECONDS = 5, 300


def hash_password(password: str) -> str:
    if len(password) < 10:
        raise ValueError("Password must be at least 10 characters.")
    salt = secrets.token_bytes(16)
    dk = hashlib.scrypt(password.encode(), salt=salt, **_SCRYPT)
    return f"scrypt${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str | None) -> bool:
    if not stored or not stored.startswith("scrypt$"):
        hashlib.scrypt(b"x", salt=b"0" * 16, **_SCRYPT)          # constant-ish time when no hash
        return False
    _, salt, dk = stored.split("$")
    test = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), **_SCRYPT)
    return hmac.compare_digest(test.hex(), dk)


def _secret() -> bytes:
    env = os.environ.get("TMPCHECK_SECRET")
    if env:
        return env.encode()
    path = ROOT / "output" / ".session_secret"            # output/ is git-ignored
    path.parent.mkdir(exist_ok=True)
    if not path.exists():
        path.write_text(secrets.token_hex(32))
    return path.read_text().strip().encode()


def _h(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def locked(email: str) -> bool:
    now = time.time()
    recent = [t for t in _failures.get(email.lower(), []) if now - t < LOCK_SECONDS]
    _failures[email.lower()] = recent
    return len(recent) >= LOCK_AFTER


def authenticate(db: Session, email: str, password: str) -> User | None:
    email = (email or "").strip().lower()
    if locked(email):
        return None
    user = db.query(User).filter(User.email == email).first()
    if user and user.active and verify_password(password, user.password_hash):
        _failures.pop(email, None)
        return user
    if not user:
        verify_password(password, None)
    _failures.setdefault(email, []).append(time.time())
    return None


def start_session(db: Session, user: User) -> str:
    token = secrets.token_urlsafe(32)
    db.add(UserSession(token_hash=_h(token), user_id=user.id,
                       expires_at=utcnow() + timedelta(hours=SESSION_HOURS)))
    db.commit()
    return token


def session_user(db: Session, token: str | None) -> User | None:
    if not token:
        return None
    s = db.query(UserSession).filter_by(token_hash=_h(token)).first()
    if not s:
        return None
    exp = s.expires_at if s.expires_at.tzinfo else s.expires_at.replace(tzinfo=utcnow().tzinfo)
    if exp < utcnow():
        db.delete(s)
        db.commit()
        return None
    user = db.get(User, s.user_id)
    return user if user and user.active else None


def end_session(db: Session, token: str | None) -> None:
    if token:
        db.query(UserSession).filter_by(token_hash=_h(token)).delete()
        db.commit()


def csrf_token(session_token: str | None) -> str:
    return hmac.new(_secret(), (session_token or "").encode(), hashlib.sha256).hexdigest()


def csrf_ok(session_token: str | None, supplied: str | None) -> bool:
    return bool(session_token and supplied) and hmac.compare_digest(csrf_token(session_token), supplied)


def is_reviewer(user: User) -> bool:
    return user.role in REVIEWER_ROLES


def audit(db: Session, user: User | None, action: str, obj: str | None = None, detail: str | None = None,
          ip: str | None = None, org_id: int | None = None) -> None:
    db.add(AuditEvent(org_id=org_id if org_id is not None else (user.org_id if user else None),
                      user_id=user.id if user else None, action=action, object=obj, detail=detail, ip=ip))
    db.commit()

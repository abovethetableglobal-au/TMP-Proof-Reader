"""Shared helpers: sign a test client in and attach its CSRF token to every request."""
from src.portal import auth

PASSWORD = "correct-horse-battery"
PW_HASH = auth.hash_password(PASSWORD)


def login(client, email: str, password: str = PASSWORD):
    client.cookies.clear()
    client.headers.pop("X-CSRF-Token", None)
    r = client.post("/login", data={"email": email, "password": password, "next": "/"}, follow_redirects=False)
    token = client.cookies.get(auth.COOKIE)
    if token:
        client.headers["X-CSRF-Token"] = auth.csrf_token(token)
    return r

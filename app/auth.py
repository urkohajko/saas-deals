from starlette.responses import RedirectResponse
from fastapi import Request
from hashlib import sha256


ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


def hash_password(password: str) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


def is_logged(request: Request) -> bool:
    return bool(request.session.get("logged_in"))


def require_login(request: Request):
    return RedirectResponse("/admin/login", status_code=303)

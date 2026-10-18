import secrets
from fastapi import Header, HTTPException
from app.config import get_settings


def require_admin(x_admin_key: str | None = Header(default=None, alias="X-Admin-Key")) -> None:
    expected = get_settings().admin_api_key
    if not expected or not x_admin_key or not secrets.compare_digest(x_admin_key, expected):
        raise HTTPException(status_code=401, detail="Invalid admin key")

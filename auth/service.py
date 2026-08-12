"""Authentication and JWT token service."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from core.config import AUTH_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
from database.users import create_user, get_user_by_id, get_user_by_username


class AuthError(Exception):
    """Raised when authentication fails."""


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def _require_secret() -> str:
    if not AUTH_SECRET:
        raise AuthError(
            "WASIFY_AUTH_SECRET is not configured. Set it in your environment or .env file."
        )
    return AUTH_SECRET


def create_access_token(user_id: int, username: str) -> str:
    secret = _require_secret()
    expire = datetime.now(UTC) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire,
    }
    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    secret = _require_secret()
    try:
        payload = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise AuthError("Invalid or expired token") from exc
    return payload


def register_user(username: str, name: str, password: str) -> dict[str, Any]:
    if not username or not name or not password:
        raise AuthError("Username, name, and password are required")

    password_hash = hash_password(password)
    created = create_user(username, name, password_hash)
    if not created:
        raise AuthError("Username already exists")

    user = get_user_by_username(username)
    if not user:
        raise AuthError("Registration failed")

    token = create_access_token(user["id"], user["username"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user["id"], "username": user["username"], "name": user["name"]},
    }


def login_user(username: str, password: str) -> dict[str, Any]:
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password_hash"]):
        raise AuthError("Invalid username or password")

    token = create_access_token(user["id"], user["username"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user["id"], "username": user["username"], "name": user["name"]},
    }


def get_current_user_from_token(token: str) -> dict[str, Any]:
    payload = decode_access_token(token)
    user_id = int(payload["sub"])
    user = get_user_by_id(user_id)
    if not user:
        raise AuthError("User not found")
    return user

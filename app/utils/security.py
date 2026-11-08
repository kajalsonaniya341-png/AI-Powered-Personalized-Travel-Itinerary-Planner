"""Password hashing (bcrypt) and JWT helpers (PyJWT)."""
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from app import config


def hash_password(password: str) -> str:
    import bcrypt  # imported here so JWT helpers work even if bcrypt is not installed

    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    import bcrypt

    try:
        return bcrypt.checkpw(password.encode("utf-8")[:72], hashed.encode("utf-8"))
    except ValueError:  # malformed hash
        return False


def create_access_token(user_id: str, expires_minutes: Optional[int] = None) -> str:
    minutes = config.ACCESS_TOKEN_EXPIRE_MINUTES if expires_minutes is None else expires_minutes
    now = datetime.now(timezone.utc)
    payload = {"sub": user_id, "iat": now, "exp": now + timedelta(minutes=minutes)}
    return jwt.encode(payload, config.require_jwt_secret(), algorithm=config.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """Return the user id inside a valid token, or None if invalid/expired/tampered."""
    try:
        payload = jwt.decode(token, config.require_jwt_secret(), algorithms=[config.JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None
    sub = payload.get("sub")
    return sub if isinstance(sub, str) else None

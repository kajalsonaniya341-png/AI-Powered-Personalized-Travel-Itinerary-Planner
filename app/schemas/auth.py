"""Request/response shapes for authentication (validated by Pydantic)."""
import re

from pydantic import BaseModel, Field, field_validator

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _check_email(value: str) -> str:
    value = value.strip().lower()
    if not EMAIL_RE.match(value) or len(value) > 254:
        raise ValueError("Enter a valid email address.")
    return value


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str
    password: str = Field(min_length=8, max_length=72)  # bcrypt only uses the first 72 bytes

    @field_validator("email")
    @classmethod
    def valid_email(cls, v):
        return _check_email(v)

    @field_validator("username")
    @classmethod
    def clean_username(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters.")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def valid_email(cls, v):
        return _check_email(v)


class UserPublic(BaseModel):
    id: str
    username: str
    email: str
    created_at: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic

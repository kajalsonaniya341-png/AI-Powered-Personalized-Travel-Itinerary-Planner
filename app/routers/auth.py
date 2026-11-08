"""Authentication routes: register, login, and the current user."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import get_db
from app.models import user as user_model
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserPublic
from app.utils.security import create_access_token, decode_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db=Depends(get_db),
) -> dict:
    """Dependency that protects routes. Returns the user document or raises 401."""
    unauthorized = HTTPException(
        status_code=401,
        detail="Please log in to continue.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Your session is invalid or has expired. Please log in again.",
                            headers={"WWW-Authenticate": "Bearer"})
    user = user_model.get_user_by_id(db, user_id)
    if user is None:
        raise unauthorized
    return user


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(body: RegisterRequest, db=Depends(get_db)):
    if user_model.get_user_by_email(db, body.email):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    try:
        doc = user_model.create_user(db, body.username, body.email, hash_password(body.password))
    except Exception as exc:
        # The unique email index is the final guard against two simultaneous sign-ups.
        if exc.__class__.__name__ == "DuplicateKeyError":
            raise HTTPException(status_code=409, detail="An account with this email already exists.")
        raise
    return TokenResponse(access_token=create_access_token(str(doc["_id"])),
                         user=UserPublic(**user_model.serialize_user(doc)))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db=Depends(get_db)):
    user = user_model.get_user_by_email(db, body.email)
    # Same message for unknown email and wrong password so accounts cannot be probed.
    if user is None or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    return TokenResponse(access_token=create_access_token(str(user["_id"])),
                         user=UserPublic(**user_model.serialize_user(user)))


@router.get("/me", response_model=UserPublic)
def me(current_user: dict = Depends(get_current_user)):
    return UserPublic(**user_model.serialize_user(current_user))

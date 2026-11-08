"""Application settings, read from environment variables (and a local .env file).

No secrets are hardcoded. See .env.example for the variables you need to set.
"""
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "AI-Powered Personalized Travel Itinerary Planner"
DB_NAME = os.getenv("MONGODB_DB_NAME", "travel_planner_db")

MONGODB_URI = os.getenv("MONGODB_URI", "")
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Optional AI layer (a real LLM). Without AI_API_KEY the AI features are simply switched off.
AI_PROVIDER = os.getenv("AI_PROVIDER", "anthropic").strip().lower()      # "anthropic" or "gemini"
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_MODEL = os.getenv("AI_MODEL", "").strip()                              # empty = provider default
AI_TIMEOUT_SECONDS = int(os.getenv("AI_TIMEOUT_SECONDS", "90"))
AI_RATE_LIMIT_PER_MINUTE = int(os.getenv("AI_RATE_LIMIT_PER_MINUTE", "10"))

# Comma-separated list of allowed browser origins, e.g. "https://my-app.onrender.com".
# The frontend is served by this same app, so the default (empty) means same-origin only.
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

# Optional: insert/update the sample dataset (safe upserts only) when the server starts.
SEED_ON_STARTUP = os.getenv("SEED_ON_STARTUP", "false").lower() == "true"


def resolve_mongodb_uri(force_prompt: bool = False) -> str:
    """Return the real connection string.

    If MONGODB_URI contains the placeholder <password>, the password is taken from
    MONGODB_PASSWORD (for servers) or typed in the terminal (VISIBLE as you type, so you
    can see what you entered) so it never has to be saved in a file. Special characters
    are URL-encoded automatically. force_prompt=True ignores MONGODB_PASSWORD (used for retries).
    """
    uri = MONGODB_URI
    if not uri:
        raise RuntimeError("MONGODB_URI is not set. Copy .env.example to .env and fill it in.")
    if "<password>" not in uri:
        return uri
    password = "" if force_prompt else os.getenv("MONGODB_PASSWORD", "")
    if not password:
        import sys

        if not sys.stdin or not sys.stdin.isatty():
            raise RuntimeError("MongoDB password needed: run in a terminal to be prompted, or set MONGODB_PASSWORD.")
        password = input("Enter MongoDB Atlas password for the database user (visible): ").strip()
    from urllib.parse import quote_plus

    return uri.replace("<password>", quote_plus(password))


def require_jwt_secret() -> str:
    """Return the JWT secret or fail loudly (never fall back to a default secret)."""
    if len(JWT_SECRET) < 16:
        raise RuntimeError("JWT_SECRET is missing or too short (use at least 16 characters). Set it in .env.")
    return JWT_SECRET

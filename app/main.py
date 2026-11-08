"""FastAPI entry point for the AI-Powered Personalized Travel Itinerary Planner.

Run locally:   uvicorn app.main:app --reload
The API lives under /api and the website (static/) is served from "/".
"""
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.database import ensure_indexes, get_client, get_db
from app.routers import ai, auth, destinations, places, trips

logger = logging.getLogger("travel_planner")
BASE_DIR = Path(__file__).resolve().parent.parent


def seed_from_file(db) -> int:
    """Idempotent upsert of data/places.json keyed on (name, city). Never deletes anything."""
    data = json.loads((BASE_DIR / "data" / "places.json").read_text(encoding="utf-8"))
    for place in data["places"]:
        db.places.update_one({"name": place["name"], "city": place["city"]}, {"$set": place}, upsert=True)
    return len(data["places"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    # A database problem at startup must not crash the server: /api/health reports it instead.
    try:
        db = get_client()[config.DB_NAME]
        db.command("ping")
        ensure_indexes(db)
        if config.SEED_ON_STARTUP:
            logger.info("Seeded %s places", seed_from_file(db))
    except Exception as exc:
        logger.error("Startup database setup failed: %s", exc)
    yield


app = FastAPI(title=config.PROJECT_NAME, version="1.0.0", lifespan=lifespan)

if config.CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS, allow_credentials=False,
                       allow_methods=["GET", "POST", "DELETE"], allow_headers=["Authorization", "Content-Type"])


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception):
    """Last-resort handler: log the real error, show the user a safe message (no traceback)."""
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Something went wrong on our side. Please try again."})


@app.get("/api/health", tags=["Health"])
def health():
    """Used by the hosting platform as a health check. 503 when MongoDB cannot be reached."""
    try:
        get_client().admin.command("ping")
        return {"status": "ok", "database": "connected", "database_name": config.DB_NAME}
    except Exception:
        return JSONResponse(status_code=503, content={"status": "degraded", "database": "unavailable"})


for module in (auth, destinations, places, trips, ai):
    app.include_router(module.router)

# Static website last, so it never shadows /api routes.
app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")

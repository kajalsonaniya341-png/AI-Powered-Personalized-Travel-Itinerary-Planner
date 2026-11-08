"""MongoDB connection (PyMongo) and index setup.

Only the database named in config.DB_NAME (travel_planner_db) is ever touched.
Nothing in this project drops databases or collections.
"""
import logging

from fastapi import HTTPException

from app import config

logger = logging.getLogger(__name__)
_client = None


def get_client():
    """Create the MongoDB client once and reuse it.

    If Atlas rejects the password, the terminal asks again (up to 3 tries).
    """
    global _client
    if _client is None:
        from pymongo import MongoClient
        from pymongo.errors import OperationFailure

        for attempt in range(1, 4):
            client = MongoClient(config.resolve_mongodb_uri(force_prompt=attempt > 1),
                                 serverSelectionTimeoutMS=8000)
            try:
                client.admin.command("ping")
                _client = client
                break
            except OperationFailure as exc:
                client.close()
                if getattr(exc, "code", None) != 8000 and "auth" not in str(exc).lower():
                    raise
                if attempt == 3:
                    raise RuntimeError("Atlas rejected the username/password 3 times. Check Database Access in Atlas.")
                print(f"Wrong username or password (try {attempt} of 3). Please enter the password again.")
    return _client


def get_db():
    """FastAPI dependency returning the database. Tests replace this with a fake."""
    try:
        client = get_client()
        client.admin.command("ping")
        return client[config.DB_NAME]
    except Exception as exc:  # connection problems must not leak tracebacks to users
        logger.error("MongoDB unavailable: %s", exc)
        raise HTTPException(status_code=503, detail="The database is currently unavailable. Please try again later.")


def ensure_indexes(db) -> None:
    """Create indexes. create_index is idempotent, so this is safe to run every startup."""
    db.users.create_index("email", unique=True)
    db.places.create_index([("name", 1), ("city", 1)], unique=True)
    db.places.create_index("city")
    db.trips.create_index([("user_id", 1), ("created_at", -1)])

"""User data access. Passwords are only ever stored as hashes."""
from datetime import datetime, timezone
from typing import Optional

from app.models.place import to_object_id


def serialize_user(doc: dict) -> dict:
    """Public view of a user. Never includes the password hash."""
    return {
        "id": str(doc["_id"]),
        "username": doc["username"],
        "email": doc["email"],
        "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
    }


def create_user(db, username: str, email: str, hashed_password: str) -> dict:
    """Insert a user. Raises pymongo DuplicateKeyError if the email exists (unique index)."""
    doc = {
        "username": username,
        "email": email.lower(),
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc),
    }
    result = db.users.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


def get_user_by_email(db, email: str) -> Optional[dict]:
    return db.users.find_one({"email": email.lower()})


def get_user_by_id(db, user_id: str) -> Optional[dict]:
    oid = to_object_id(user_id)
    return db.users.find_one({"_id": oid}) if oid else None

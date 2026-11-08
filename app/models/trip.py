"""Saved-trip data access. Every query is scoped to the owning user_id."""
from datetime import datetime, timezone
from typing import Optional

from app.models.place import to_object_id


def serialize_trip(doc: dict, include_itinerary: bool = True) -> dict:
    data = {
        "id": str(doc["_id"]),
        "destination": doc["destination"],
        "days": doc["days"],
        "budget": doc["budget"],
        "travelers": doc["travelers"],
        "interests": doc["interests"],
        "estimated_total_cost": doc["estimated_total_cost"],
        "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
    }
    full = (doc.get("itinerary") or {}).get("full_trip_cost") or {}
    data["estimated_full_cost"] = full.get("total")  # None for trips saved before this feature
    if include_itinerary:
        data["itinerary"] = doc["itinerary"]
    return data


def create_trip(db, user_id: str, payload: dict) -> dict:
    doc = {
        "user_id": user_id,
        "destination": payload["destination"],
        "days": payload["days"],
        "budget": payload["budget"],
        "travelers": payload["travelers"],
        "interests": payload["interests"],
        "itinerary": payload["itinerary"],
        "estimated_total_cost": payload["estimated_total_cost"],
        "created_at": datetime.now(timezone.utc),
    }
    result = db.trips.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


def list_trips(db, user_id: str) -> list:
    docs = sorted(db.trips.find({"user_id": user_id}), key=lambda d: d["created_at"], reverse=True)
    return [serialize_trip(d, include_itinerary=False) for d in docs]


def get_trip(db, user_id: str, trip_id: str) -> Optional[dict]:
    oid = to_object_id(trip_id)
    if oid is None:
        return None
    doc = db.trips.find_one({"_id": oid, "user_id": user_id})
    return serialize_trip(doc) if doc else None


def delete_trip(db, user_id: str, trip_id: str) -> bool:
    oid = to_object_id(trip_id)
    if oid is None:
        return False
    return db.trips.delete_one({"_id": oid, "user_id": user_id}).deleted_count == 1

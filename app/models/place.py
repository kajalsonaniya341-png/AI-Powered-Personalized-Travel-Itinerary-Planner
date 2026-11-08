"""Place data access + helpers. All MongoDB reads/writes for places live here."""
from typing import Optional

VALID_CATEGORIES = {
    "history", "adventure", "nature", "food", "culture", "shopping",
    "religious", "museums", "wildlife", "architecture",
}
REQUIRED_FIELDS = ("name", "city", "state", "categories", "description", "cost", "hours",
                   "rating", "latitude", "longitude", "source", "verified")


def validate_place_doc(doc: dict) -> list:
    """Return a list of problems with a place document (empty list = OK)."""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in doc:
            errors.append(f"missing field '{field}'")
    if errors:
        return errors
    if not doc["name"] or not doc["city"]:
        errors.append("name and city must not be empty")
    unknown = set(doc["categories"]) - VALID_CATEGORIES
    if unknown:
        errors.append(f"unknown categories {sorted(unknown)}")
    if doc["cost"] is not None and doc["cost"] < 0:
        errors.append("cost must not be negative")
    if not doc["hours"] or doc["hours"] <= 0:
        errors.append("hours must be positive")
    if doc["rating"] is not None and not (0 <= doc["rating"] <= 5):
        errors.append("rating must be between 0 and 5 or null")
    lat, lon = doc["latitude"], doc["longitude"]
    if (lat is None) != (lon is None):
        errors.append("latitude and longitude must both be set or both be null")
    if lat is not None and lon is not None and not (-90 <= lat <= 90 and -180 <= lon <= 180):
        errors.append("coordinates out of range")
    return errors


def serialize_place(doc: dict) -> dict:
    """Convert a MongoDB document to a JSON-safe dict (ObjectId -> string id)."""
    return {
        "id": str(doc.get("_id", "")),
        "name": doc["name"],
        "city": doc["city"],
        "state": doc.get("state"),
        "categories": doc.get("categories", []),
        "description": doc.get("description", ""),
        "cost": doc.get("cost"),
        "cost_is_estimate": doc.get("cost_is_estimate", True),
        "hours": doc.get("hours"),
        "hours_is_estimate": doc.get("hours_is_estimate", True),
        "rating": doc.get("rating"),
        "latitude": doc.get("latitude"),
        "longitude": doc.get("longitude"),
        "coordinates_approximate": doc.get("coordinates_approximate", False),
        "source": doc.get("source", "sample_dataset"),
        "verified": doc.get("verified", False),
    }


def to_object_id(value: str):
    """Parse a string into an ObjectId, or return None if it is not a valid id."""
    from bson import ObjectId
    from bson.errors import InvalidId

    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def is_object_id(value: str) -> bool:
    return len(value) == 24 and all(c in "0123456789abcdefABCDEF" for c in value)


def find_places(db, city: Optional[str] = None) -> list:
    query = {"city": city} if city else {}
    return [serialize_place(d) for d in db.places.find(query)]


def find_place_by_id(db, place_id: str) -> Optional[dict]:
    oid = to_object_id(place_id)
    if oid is None:
        return None
    doc = db.places.find_one({"_id": oid})
    return serialize_place(doc) if doc else None


def list_cities(db) -> list:
    """Summary per destination: city, state, place count, categories available."""
    cities = {}
    for doc in db.places.find({}):
        entry = cities.setdefault(doc["city"], {"city": doc["city"], "state": doc.get("state"),
                                                "place_count": 0, "categories": set(), "interest_counts": {}})
        entry["place_count"] += 1
        entry["categories"].update(doc.get("categories", []))
        for cat in set(doc.get("categories", [])):  # how many attractions match each interest in this destination
            entry["interest_counts"][cat] = entry["interest_counts"].get(cat, 0) + 1
    result = []
    for entry in sorted(cities.values(), key=lambda e: e["city"]):
        entry["categories"] = sorted(entry["categories"])
        result.append(entry)
    return result


def match_city(db, name: str) -> Optional[str]:
    """Case-insensitive lookup of the canonical city name, or None."""
    wanted = name.strip().lower()
    for entry in list_cities(db):
        if entry["city"].lower() == wanted:
            return entry["city"]
    return None

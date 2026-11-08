"""Load data/places.json into MongoDB (travel_planner_db.places).

Usage (from the project root):
    python -m scripts.seed_database             # write to MongoDB using MONGODB_URI
    python -m scripts.seed_database --dry-run   # only validate the JSON, no database needed

Safety: uses upserts keyed on (name, city). It never deletes or drops anything, so it
can be re-run any number of times without creating duplicates.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.models.place import validate_place_doc  # noqa: E402


def load_places() -> list:
    data = json.loads((ROOT / "data" / "places.json").read_text(encoding="utf-8"))
    places = data["places"]
    problems = []
    seen = set()
    for place in places:
        for err in validate_place_doc(place):
            problems.append(f"{place.get('name', '?')}: {err}")
        key = (place.get("name"), place.get("city"))
        if key in seen:
            problems.append(f"duplicate entry {key}")
        seen.add(key)
    if problems:
        raise SystemExit("Dataset problems:\n  " + "\n  ".join(problems))
    return places


def main() -> None:
    places = load_places()
    print(f"Dataset OK: {len(places)} places, "
          f"{len({p['city'] for p in places})} cities.")
    if "--dry-run" in sys.argv:
        print("Dry run: nothing written to MongoDB.")
        return

    from app import config
    from app.database import ensure_indexes, get_client

    db = get_client()[config.DB_NAME]
    db.command("ping")
    ensure_indexes(db)
    inserted = updated = 0
    for place in places:
        result = db.places.update_one({"name": place["name"], "city": place["city"]},
                                      {"$set": place}, upsert=True)
        if result.upserted_id is not None:
            inserted += 1
        elif result.modified_count:
            updated += 1
    print(f"Database '{config.DB_NAME}': {inserted} inserted, {updated} updated, "
          f"{len(places) - inserted - updated} unchanged.")


if __name__ == "__main__":
    main()

"""Checks on data/places.json and the project's naming/safety rules."""
import json
import subprocess
import sys
from pathlib import Path

from app.models.place import validate_place_doc
from tests.conftest import ROOT, load_sample_places


def test_every_place_is_valid():
    for place in load_sample_places():
        assert validate_place_doc(place) == [], place["name"]


INDIA_STATES_AND_UTS = {
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
}
SPEC_ATTRACTIONS = {
    "Jaipur": {"Amber Fort", "City Palace", "Hawa Mahal", "Jantar Mantar", "Jal Mahal", "Albert Hall Museum", "Chokhi Dhani"},
    "Delhi": {"Red Fort", "India Gate", "National Museum", "Lotus Temple", "Chandni Chowk", "Qutub Minar"},
    "Bhopal": {"Upper Lake", "Van Vihar National Park", "Tribal Museum", "Taj-ul-Masajid",
               "Indira Gandhi Rashtriya Manav Sangrahalaya"},
}


def test_spec_attractions_present():
    places = load_sample_places()
    for city, names in SPEC_ATTRACTIONS.items():
        assert {p["name"] for p in places if p["city"] == city} == names


def test_every_state_and_union_territory_covered():
    places = load_sample_places()
    assert {p["state"] for p in places} == INDIA_STATES_AND_UTS


def test_each_destination_belongs_to_one_state():
    owner = {}
    for p in load_sample_places():
        assert owner.setdefault(p["city"], p["state"]) == p["state"], p["city"]


def test_every_interest_has_places():
    from app.schemas.itinerary import ALLOWED_INTERESTS

    used = {c for p in load_sample_places() for c in p["categories"]}
    assert ALLOWED_INTERESTS <= used


def test_dataset_is_in_sync_with_source():
    from scripts.build_dataset import build

    assert build()["places"] == json.loads((ROOT / "data" / "places.json").read_text(encoding="utf-8"))["places"]


def test_no_invented_ratings_or_verification():
    for p in load_sample_places():
        assert p["rating"] is None
        assert p["verified"] is False
        assert p["source"] == "sample_dataset"


def test_no_duplicate_name_city_pairs():
    keys = [(p["name"], p["city"]) for p in load_sample_places()]
    assert len(keys) == len(set(keys))


def test_missing_coordinates_are_null_pairs():
    for p in load_sample_places():
        assert (p["latitude"] is None) == (p["longitude"] is None)


def test_validator_catches_problems():
    bad = {"name": "X", "city": "Y", "state": "Z", "categories": ["bogus"], "description": "", "cost": -1,
           "hours": 0, "rating": 9, "latitude": 10, "longitude": None, "source": "s", "verified": False}
    assert len(validate_place_doc(bad)) >= 5


def test_seed_script_dry_run_needs_no_database():
    result = subprocess.run([sys.executable, "-m", "scripts.seed_database", "--dry-run"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert f"{len(load_sample_places())} places" in result.stdout


def test_forbidden_brand_name_absent():
    forbidden = "Wander" + "Wise"
    for path in Path(ROOT).rglob("*"):
        if path.is_file() and path.suffix in {".py", ".js", ".html", ".css", ".md", ".json", ".txt", ".yaml", ".yml"}:
            assert forbidden.lower() not in path.read_text(encoding="utf-8", errors="ignore").lower(), path


def test_interest_counts_follow_the_destination():
    from app.models.place import list_cities
    from tests.conftest import FakeDB

    db = FakeDB()
    db.places.docs.extend(dict(p) for p in load_sample_places())
    cities = {c["city"]: c for c in list_cities(db)}
    ujjain = cities["Ujjain"]["interest_counts"]
    assert ujjain["religious"] == 4 and ujjain["culture"] >= 1
    assert "history" not in ujjain and "wildlife" not in ujjain          # nothing historic/wildlife there in the dataset
    assert cities["Ranthambore"]["interest_counts"]["wildlife"] >= 1
    assert "wildlife" not in cities["Jaipur"]["interest_counts"]
    assert cities["Jaipur"]["interest_counts"]["history"] == 5

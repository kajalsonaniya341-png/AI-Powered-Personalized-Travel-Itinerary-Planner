"""Generate data/places.json from scripts/dataset_source.py.

    python -m scripts.build_dataset

The output keeps every honesty flag explicit: costs/hours are estimates, coordinates are
approximate (or null), ratings are null, nothing is verified.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.dataset_source import DESTINATIONS  # noqa: E402


def build() -> dict:
    places = []
    for state, city, items in DESTINATIONS:
        for name, cats, cost, hours, lat, lon, desc in items:
            places.append({
                "name": name,
                "city": city,
                "state": state,
                "categories": cats.split(),
                "description": desc,
                "cost": cost,
                "cost_is_estimate": True,
                "hours": hours,
                "hours_is_estimate": True,
                "rating": None,
                "latitude": lat,
                "longitude": lon,
                "coordinates_approximate": lat is not None,
                "source": "sample_dataset",
                "verified": False,
            })
    return {
        "meta": {
            "name": "AI-Powered Personalized Travel Itinerary Planner - sample dataset (India)",
            "currency": "INR",
            "coverage": "All 28 states and 8 union territories, with selected major destinations in each. Not exhaustive.",
            "notice": "SAMPLE DATA. Costs and visit durations are rough estimates, coordinates are approximate "
                      "(null when unknown), ratings are intentionally null. Nothing is live or officially verified. "
                      "Check opening hours, tickets and access rules before travelling.",
            "version": 2,
        },
        "places": places,
    }


if __name__ == "__main__":
    data = build()
    out = ROOT / "data" / "places.json"
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    cities = {p["city"] for p in data["places"]}
    states = {p["state"] for p in data["places"]}
    print(f"Wrote {len(data['places'])} places, {len(cities)} destinations, {len(states)} states/UTs -> {out}")

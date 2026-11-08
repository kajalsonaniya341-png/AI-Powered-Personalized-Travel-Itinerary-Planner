"""Turns ranked places into a realistic day-by-day itinerary (structured JSON).

This module is pure Python and does not talk to the database: the router reads the
places from MongoDB and passes them in. That keeps it easy to test and to replace.
"""
import math
from typing import Optional
from urllib.parse import quote_plus

from app.services import ml
from app.services.budget import estimate_trip_cost, style_alternatives
from app.services.recommendation import ATTRACTION_BUDGET_SHARE, WEIGHTS, rank_places

MAX_PLACES_PER_DAY = {"budget": 4, "balanced": 3, "luxury": 3}
MAX_HOURS_PER_DAY = 7.0
COST_DISCLAIMER = (
    "Estimated costs cover attraction entry fees only (cost per person x travelers), based on a "
    "sample dataset. They exclude stay, food and transport and are not official ticket prices."
)


class NoPlacesError(Exception):
    """Raised when there are no places for the requested destination."""


def _distance_km(a: dict, b: dict) -> Optional[float]:
    """Straight-line (haversine) distance, used ONLY to group nearby places in a day.
    It is not a road distance and is never shown to users as one."""
    if None in (a.get("latitude"), a.get("longitude"), b.get("latitude"), b.get("longitude")):
        return None
    lat1, lon1, lat2, lon2 = map(math.radians, (a["latitude"], a["longitude"], b["latitude"], b["longitude"]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def map_url(place: dict) -> str:
    """OpenStreetMap link. Uses stored coordinates if present, otherwise a name search (no invented coords)."""
    if place.get("latitude") is not None and place.get("longitude") is not None:
        lat, lon = place["latitude"], place["longitude"]
        return f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}"
    return "https://www.openstreetmap.org/search?query=" + quote_plus(f"{place['name']} {place['city']}")


def _public_place(place: dict, travelers: int) -> dict:
    cost = place.get("cost")
    return {
        "id": place.get("id"),
        "name": place["name"],
        "city": place["city"],
        "state": place.get("state"),
        "categories": place["categories"],
        "description": place["description"],
        "cost_per_person": cost,
        "cost_is_estimate": place.get("cost_is_estimate", True),
        "entry_cost_total": None if cost is None else round(cost * travelers, 2),
        "hours": place.get("hours"),
        "hours_is_estimate": place.get("hours_is_estimate", True),
        "rating": place.get("rating"),
        "latitude": place.get("latitude"),
        "longitude": place.get("longitude"),
        "coordinates_approximate": place.get("coordinates_approximate", False),
        "map_url": map_url(place),
        "source": place.get("source", "sample_dataset"),
        "verified": place.get("verified", False),
        "score": place["score"],
        "matched_interests": place["matched_interests"],
    }


def _pick_for_day(remaining: list, max_places: int, remaining_budget: float, travelers: int) -> list:
    """Greedily fill one day: best-ranked place first, then prefer high scores that are close by."""
    day, hours_used, spent = [], 0.0, 0.0
    candidates = list(remaining)
    while candidates and len(day) < max_places:
        anchor = day[0] if day else None

        def key(p):
            bonus = 0.0
            if anchor is not None:
                d = _distance_km(anchor, p)
                if d is not None:
                    bonus = -0.01 * d  # slightly prefer places near the first stop
            return p["score"] + bonus

        chosen = None
        for p in sorted(candidates, key=key, reverse=True):
            cost_total = (p.get("cost") or 0) * travelers
            hours = p.get("hours") or 1
            fits_hours = hours_used + hours <= MAX_HOURS_PER_DAY or not day
            fits_budget = spent + cost_total <= remaining_budget
            if fits_hours and fits_budget:
                chosen = p
                break
        if chosen is None:
            break
        day.append(chosen)
        candidates.remove(chosen)
        hours_used += chosen.get("hours") or 1
        spent += (chosen.get("cost") or 0) * travelers
    return day


def build_itinerary(places: list, destination: str, days: int, budget: float,
                    travelers: int, interests: list, travel_style: str = "balanced",
                    nights: Optional[int] = None, travel_cost_per_person: float = 0.0,
                    travel_mode: str = "none", ml_model=None) -> dict:
    """Rank places, then split them across days. Never repeats a place."""
    if not places:
        raise NoPlacesError(f"No attractions are available for '{destination}'.")

    ranked = rank_places(places, interests, budget, travelers, days, travel_style)
    ml_used = ml.blend(ranked, ml_model, interests)  # optional ML layer; rules alone if unavailable
    max_places = MAX_PLACES_PER_DAY.get(travel_style, 3)

    remaining = ranked
    spent_so_far = 0.0
    daily_plan = []
    for day_number in range(1, days + 1):
        picked = _pick_for_day(remaining, max_places, budget - spent_so_far, travelers)
        if not picked:
            break
        picked_ids = {p["name"] for p in picked}
        remaining = [p for p in remaining if p["name"] not in picked_ids]
        day_cost = sum((p.get("cost") or 0) * travelers for p in picked)
        spent_so_far += day_cost
        daily_plan.append({
            "day": day_number,
            "places": [_public_place(p, travelers) for p in picked],
            "total_hours": round(sum(p.get("hours") or 1 for p in picked), 1),
            "estimated_cost": round(day_cost, 2),
        })

    warnings, notes = [], []
    if len(daily_plan) < days:
        notes.append(
            f"Only {len(daily_plan)} of {days} days could be filled: the sample dataset has "
            f"{len(places)} attractions for {destination} and each is used at most once."
        )
    left_out = [p["name"] for p in remaining]
    over_budget = [p["name"] for p in remaining
                   if (p.get("cost") or 0) * travelers > max(0.0, budget - spent_so_far)]
    if over_budget:
        warnings.append("Skipped to stay within your budget: " + ", ".join(over_budget) + ".")
    unmatched = [i for i in interests if not any(i in p["categories"] for p in places)]
    if unmatched:
        notes.append("No attractions tagged for: " + ", ".join(unmatched) + " in this destination.")
    if left_out and not over_budget:
        notes.append("Not scheduled (limited by days or daily time): " + ", ".join(left_out) + ".")
    missing_coords = sum(1 for d in daily_plan for p in d["places"] if p["latitude"] is None)
    if missing_coords:
        notes.append(f"{missing_coords} attraction(s) have no stored coordinates, so they are not on the map.")

    total = round(sum(d["estimated_cost"] for d in daily_plan), 2)
    full = estimate_trip_cost(destination, days, travelers, travel_style, total, nights, travel_cost_per_person, budget, travel_mode)
    full["alternatives"] = style_alternatives(destination, days, travelers, total, nights, travel_cost_per_person)
    if not full["within_budget"]:
        warnings.append(f"Your estimated full trip cost (about ₹{full['total']:,}) is above your budget of ₹{budget:,.0f}. "
                        f"The cheapest style (Budget) would be about ₹{full['alternatives']['budget']:,}.")
    return {
        "destination": destination,
        "days": days,
        "budget": budget,
        "travelers": travelers,
        "interests": interests,
        "travel_style": travel_style,
        "daily_plan": daily_plan,
        "estimated_total_cost": total,
        "remaining_budget_after_entry_fees": round(budget - total, 2),
        "attraction_budget_guideline": round(budget * ATTRACTION_BUDGET_SHARE, 2),
        "within_budget": total <= budget,
        "full_trip_cost": full,
        "cost_disclaimer": COST_DISCLAIMER,
        "warnings": warnings,
        "notes": notes,
        "algorithm": {
            "type": "rules_plus_ml_text_similarity" if ml_used else "rule_based_scoring",
            "is_machine_learning": ml_used,
            "weights": WEIGHTS,
            "note": "Rating weight is redistributed when a place has no reliable rating.",
            "ml": {
                "used": ml_used,
                "method": ml.METHOD,
                "weight": ml.ML_WEIGHT,
                "trained_on_places": ml_model.n_places if ml_used else 0,
                "note": ("The ML part gets 20% of the final score and learns only from the sample "
                         "dataset text; the rules keep 80%." if ml_used else
                         "ML layer not used (scikit-learn unavailable); rules only."),
            },
        },
    }

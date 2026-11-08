"""Rule-based recommendation engine.

IMPORTANT: this is a transparent, rule-based SCORING algorithm. It is NOT a trained
machine-learning model. The functions below are small and separate so a real ML model
or an LLM-based ranker can later replace `score_place` without touching the rest.

Each place gets a score from 0 to 1 made of four parts:

    interest match    50%  - how many of the traveller's interests the place covers
    budget fit        20%  - how cheap the entry is compared with the trip budget
    rating / quality  20%  - ONLY when the place has a reliable rating (otherwise skipped)
    style fit         10%  - does the place suit Budget / Balanced / Luxury travel

When a place has no rating, its 20% is NOT invented. The remaining weights are scaled
up proportionally so the score is still out of 1 (see `score_place`).
"""
from typing import Optional

WEIGHTS = {"interest": 0.50, "budget": 0.20, "rating": 0.20, "style": 0.10}

# Share of the total trip budget we consider "available for attraction entry fees".
# The rest is assumed to go to stay, food and local transport.
ATTRACTION_BUDGET_SHARE = 0.30
MAX_ASSUMED_PLACES_PER_DAY = 3


def interest_score(place: dict, interests: list) -> tuple:
    """Return (score 0-1, list of matched interests)."""
    matched = [i for i in interests if i in place.get("categories", [])]
    if not interests:
        return 0.0, matched
    # Matching 2 interests already counts as a perfect match, so people who pick
    # many interests are not punished for places that cover only a few of them.
    target = min(len(interests), 2)
    return min(1.0, len(matched) / target), matched


def budget_score(place: dict, budget: float, travelers: int, days: int) -> float:
    """1.0 = free or very cheap for this budget, 0.0 = too expensive. Unknown cost = 0.5."""
    cost = place.get("cost")
    if cost is None:
        return 0.5
    if cost == 0:
        return 1.0
    allowance = budget * ATTRACTION_BUDGET_SHARE / max(1, days * MAX_ASSUMED_PLACES_PER_DAY)
    return max(0.0, 1.0 - (cost * travelers) / allowance)


def style_score(place: dict, travel_style: str) -> float:
    """Heuristic: budget travellers prefer cheap places, luxury travellers prefer longer visits."""
    cost = place.get("cost") or 0
    hours = place.get("hours") or 1
    if travel_style == "budget":
        return 1.0 - min(1.0, cost / 500)
    if travel_style == "luxury":
        return min(1.0, hours / 3)
    return 0.7  # balanced: no strong preference


def rating_score(place: dict) -> Optional[float]:
    """Rating on a 0-1 scale, or None when there is no reliable rating."""
    rating = place.get("rating")
    if rating is None:
        return None
    return max(0.0, min(1.0, rating / 5))


def score_place(place: dict, interests: list, budget: float, travelers: int,
                days: int, travel_style: str) -> dict:
    """Score one place. Returns the score and an explanation of each component."""
    i_score, matched = interest_score(place, interests)
    parts = {
        "interest": i_score,
        "budget": budget_score(place, budget, travelers, days),
        "style": style_score(place, travel_style),
    }
    r_score = rating_score(place)
    if r_score is not None:
        parts["rating"] = r_score

    # Only use weights for components that actually have data, then rescale to sum to 1.
    used_weight = sum(WEIGHTS[name] for name in parts)
    total = sum(WEIGHTS[name] * value for name, value in parts.items()) / used_weight
    return {
        "score": round(total, 4),
        "matched_interests": matched,
        "components": {k: round(v, 3) for k, v in parts.items()},
        "rating_used": r_score is not None,
    }


def rank_places(places: list, interests: list, budget: float, travelers: int,
                days: int, travel_style: str) -> list:
    """Return places (copies) with scoring info, best first. Ties broken by name for stability."""
    ranked = []
    for place in places:
        info = score_place(place, interests, budget, travelers, days, travel_style)
        ranked.append({**place, **info})
    ranked.sort(key=lambda p: (-p["score"], p["name"]))
    return ranked

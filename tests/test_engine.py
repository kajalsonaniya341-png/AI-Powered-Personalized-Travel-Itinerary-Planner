"""Tests for the recommendation engine and itinerary builder (pure Python, no server/DB)."""
import pytest

from app.services.itinerary import MAX_HOURS_PER_DAY, MAX_PLACES_PER_DAY, NoPlacesError, build_itinerary, map_url
from app.services.recommendation import WEIGHTS, rank_places, score_place


def jaipur(sample_places):
    return [p for p in sample_places if p["city"] == "Jaipur"]


def test_weights_sum_to_one():
    assert sum(WEIGHTS.values()) == pytest.approx(1.0)


def test_interest_match_ranks_higher(sample_places):
    ranked = rank_places(jaipur(sample_places), ["food"], 20000, 2, 3, "balanced")
    assert ranked[0]["name"] == "Chokhi Dhani"  # the only Jaipur place tagged "food"


def test_no_rating_does_not_invent_rating(sample_places):
    info = score_place(jaipur(sample_places)[0], ["history"], 15000, 2, 3, "balanced")
    assert info["rating_used"] is False
    assert "rating" not in info["components"]
    assert 0 <= info["score"] <= 1


def test_rating_weight_used_only_when_present():
    place = {"name": "X", "city": "C", "categories": ["history"], "cost": 0, "hours": 1}
    plain = score_place(place, ["history"], 10000, 1, 1, "balanced")
    rated = score_place({**place, "rating": 5}, ["history"], 10000, 1, 1, "balanced")
    assert rated["rating_used"] is True and "rating" in rated["components"]
    assert plain["score"] == pytest.approx(1 * 0.5 / 0.8 + 1 * 0.2 / 0.8 + 0.7 * 0.1 / 0.8, abs=1e-3)  # rescaled
    assert rated["score"] > plain["score"] - 1e-9


def test_scores_stay_between_0_and_1(sample_places):
    for p in rank_places(sample_places, ["history", "food"], 500, 10, 7, "luxury"):
        assert 0 <= p["score"] <= 1


def test_budget_affects_ranking_for_expensive_place():
    cheap = {"name": "Cheap", "city": "C", "categories": ["food"], "cost": 0, "hours": 1}
    pricey = {"name": "Pricey", "city": "C", "categories": ["food"], "cost": 800, "hours": 1}
    ranked = rank_places([pricey, cheap], ["food"], 3000, 2, 2, "balanced")
    assert ranked[0]["name"] == "Cheap"


def test_itinerary_has_no_duplicate_places(sample_places):
    plan = build_itinerary(jaipur(sample_places), "Jaipur", 7, 50000, 2, ["history"], "balanced")
    names = [p["name"] for d in plan["daily_plan"] for p in d["places"]]
    assert len(names) == len(set(names))


def test_daily_limits_respected(sample_places):
    plan = build_itinerary(jaipur(sample_places), "Jaipur", 3, 50000, 2, ["history", "culture"], "balanced")
    for day in plan["daily_plan"]:
        assert len(day["places"]) <= MAX_PLACES_PER_DAY["balanced"]
        assert day["total_hours"] <= MAX_HOURS_PER_DAY or len(day["places"]) == 1


def test_costs_add_up(sample_places):
    plan = build_itinerary(jaipur(sample_places), "Jaipur", 3, 50000, 3, ["history"], "balanced")
    total = 0
    for d in plan["daily_plan"]:
        assert d["estimated_cost"] == pytest.approx(sum(p["entry_cost_total"] for p in d["places"]))
        total += d["estimated_cost"]
    assert plan["estimated_total_cost"] == pytest.approx(total)
    assert plan["within_budget"] is True


def test_tiny_budget_is_respected(sample_places):
    plan = build_itinerary(jaipur(sample_places), "Jaipur", 3, 120, 2, ["history"], "balanced")
    assert plan["estimated_total_cost"] <= 120
    assert plan["warnings"], "should explain which places were skipped for budget"


def test_more_days_than_places_adds_note(sample_places):
    delhi = [p for p in sample_places if p["city"] == "Bhopal"]  # 5 places
    plan = build_itinerary(delhi, "Bhopal", 7, 50000, 1, ["museums"], "balanced")
    assert len(plan["daily_plan"]) < 7
    assert any("Only" in n for n in plan["notes"])


def test_unmatched_interest_is_reported(sample_places):
    plan = build_itinerary(jaipur(sample_places), "Jaipur", 2, 20000, 2, ["wildlife"], "balanced")
    assert any("wildlife" in n for n in plan["notes"])


def test_no_places_raises():
    with pytest.raises(NoPlacesError):
        build_itinerary([], "Nowhere", 2, 1000, 1, ["history"], "balanced")


def test_missing_coordinates_not_invented(sample_places):
    chokhi = next(p for p in sample_places if p["name"] == "Chokhi Dhani")
    assert chokhi["latitude"] is None
    assert "search?query=" in map_url(chokhi)
    plan = build_itinerary(jaipur(sample_places), "Jaipur", 3, 50000, 2, ["food"], "balanced")
    out = next(p for d in plan["daily_plan"] for p in d["places"] if p["name"] == "Chokhi Dhani")
    assert out["latitude"] is None and out["longitude"] is None


def test_output_declares_rule_based_not_ml(sample_places):
    plan = build_itinerary(jaipur(sample_places), "Jaipur", 2, 20000, 2, ["history"], "budget")
    assert plan["algorithm"]["is_machine_learning"] is False
    assert plan["cost_disclaimer"]

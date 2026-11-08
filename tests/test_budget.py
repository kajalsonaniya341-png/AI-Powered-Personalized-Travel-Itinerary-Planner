"""Full trip cost estimator tests (pure Python)."""
import pytest

from app.services.budget import PEOPLE_PER_ROOM, destination_tier, estimate_trip_cost, style_alternatives
from app.services.itinerary import build_itinerary


def amounts(r):
    return {b["key"]: b["amount"] for b in r["breakdown"]}


def test_known_calculation_agra_balanced():
    r = estimate_trip_cost("Agra", 3, 2, "balanced", 420, budget=10000)
    a = amounts(r)
    assert a["stay"] == 2 * 3000            # 1 room x 2 nights x 3000
    assert a["food"] == 2 * 3 * 700
    assert a["local_transport"] == 3 * 800
    assert a["entry_fees"] == 420 and a["travel_to"] == 0
    subtotal = 6000 + 4200 + 2400 + 420
    assert a["extras"] == round(subtotal * 0.10) and r["total"] == round(subtotal * 1.10)
    assert r["within_budget"] is False and r["difference"] == r["total"] - 10000


def test_total_equals_sum_of_rows():
    r = estimate_trip_cost("Delhi", 5, 3, "luxury", 1234, travel_cost_per_person=4500, budget=1)
    assert r["total"] == sum(b["amount"] for b in r["breakdown"]) or abs(r["total"] - sum(b["amount"] for b in r["breakdown"])) <= 1


def test_rooms_and_vehicles_round_up():
    r = estimate_trip_cost("Jaipur", 2, 5, "budget", 0)   # 5 people -> 3 rooms, 2 vehicles
    assert amounts(r)["stay"] == 3 * 1 * 1500
    assert amounts(r)["local_transport"] == 2 * 2 * 350
    assert PEOPLE_PER_ROOM == 2


def test_day_trip_has_no_stay_cost_and_custom_nights():
    assert amounts(estimate_trip_cost("Jaipur", 1, 2, "balanced", 0))["stay"] == 0
    assert amounts(estimate_trip_cost("Jaipur", 3, 2, "balanced", 0, nights=3))["stay"] == 3 * 3000


def test_user_travel_cost_is_per_person_times_travelers():
    r = estimate_trip_cost("Goa", 3, 4, "balanced", 0, travel_cost_per_person=2500)
    assert amounts(r)["travel_to"] == 10000


def test_styles_get_more_expensive_and_alternatives_match():
    alt = style_alternatives("Jaipur", 3, 2, 500)
    assert alt["budget"] < alt["balanced"] < alt["luxury"]
    assert alt["balanced"] == estimate_trip_cost("Jaipur", 3, 2, "balanced", 500)["total"]


def test_destination_tiers():
    assert (destination_tier("Mumbai"), destination_tier("Jaipur"), destination_tier("Raipur")) == ("metro", "tourist", "standard")


def test_unknown_style_falls_back_to_balanced():
    assert estimate_trip_cost("Agra", 2, 2, "weird", 0)["style"] == "balanced"


def test_assumptions_say_estimates():
    assert any("not live prices" in a for a in estimate_trip_cost("Agra", 2, 2, "budget", 0)["assumptions"])


def test_itinerary_includes_full_cost_and_over_budget_warning(sample_places):
    jaipur = [p for p in sample_places if p["city"] == "Jaipur"]
    plan = build_itinerary(jaipur, "Jaipur", 3, 5000, 2, ["history"], "balanced")
    full = plan["full_trip_cost"]
    assert full["total"] > 5000 and full["within_budget"] is False
    assert any("above your budget" in w for w in plan["warnings"])
    assert full["alternatives"]["budget"] < full["alternatives"]["luxury"]
    assert amounts(full)["entry_fees"] == plan["estimated_total_cost"]


def test_itinerary_within_budget_has_no_over_warning(sample_places):
    jaipur = [p for p in sample_places if p["city"] == "Jaipur"]
    plan = build_itinerary(jaipur, "Jaipur", 2, 100000, 2, ["history"], "budget", travel_cost_per_person=2000)
    assert plan["full_trip_cost"]["within_budget"] is True
    assert not any("above your budget" in w for w in plan["warnings"])
    assert amounts(plan["full_trip_cost"])["travel_to"] == 4000


def test_travel_mode_appears_in_label_and_result():
    r = estimate_trip_cost("Goa", 3, 2, "balanced", 0, travel_cost_per_person=4000, travel_mode="train")
    row = next(b for b in r["breakdown"] if b["key"] == "travel_to")
    assert "by train" in row["label"] and row["amount"] == 8000 and r["travel_mode"] == "train"
    plain = next(b for b in estimate_trip_cost("Goa", 3, 2, "balanced", 0)["breakdown"] if b["key"] == "travel_to")
    assert "by" not in plain["label"] and plain["amount"] == 0

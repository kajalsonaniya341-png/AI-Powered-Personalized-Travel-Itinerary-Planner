"""Itinerary generation and saved-trip API tests."""
import pytest

from tests.conftest import PLAN_BODY


def test_plan_success(client):
    r = client.post("/api/plan", json=PLAN_BODY)
    assert r.status_code == 200
    plan = r.json()
    assert plan["destination"] == "Jaipur" and 1 <= len(plan["daily_plan"]) <= 3
    names = [p["name"] for d in plan["daily_plan"] for p in d["places"]]
    assert len(names) == len(set(names))
    from app.services import ml
    assert plan["algorithm"]["is_machine_learning"] is ml.is_available()
    assert plan["algorithm"]["weights"]


def test_plan_uses_database_data(client, fake_db):
    fake_db.places.docs[:] = [d for d in fake_db.places.docs if d["name"] != "Amber Fort"]
    plan = client.post("/api/plan", json={**PLAN_BODY, "days": 7, "budget": 90000}).json()
    assert "Amber Fort" not in [p["name"] for d in plan["daily_plan"] for p in d["places"]]


@pytest.mark.parametrize("override", [
    {"travel_mode": "rocket"}, {"nights": 30}, {"nights": -1}, {"travel_cost_per_person": -5}, {"budget": 0}, {"budget": -500}, {"budget": "abc"}, {"days": 0}, {"days": 8},
    {"travelers": 0}, {"interests": []}, {"interests": ["skydiving"]}, {"travel_style": "extreme"},
])
def test_plan_rejects_invalid_input(client, override):
    assert client.post("/api/plan", json={**PLAN_BODY, **override}).status_code == 422


def test_plan_returns_full_trip_cost_with_options(client):
    r = client.post("/api/plan", json={**PLAN_BODY, "nights": 2, "travel_cost_per_person": 3000, "travel_mode": "Flight"})
    assert r.status_code == 200
    assert r.json()["full_trip_cost"]["travel_mode"] == "flight"
    full = r.json()["full_trip_cost"]
    assert {b["key"] for b in full["breakdown"]} >= {"stay", "food", "local_transport", "entry_fees", "travel_to", "extras"}
    assert [b["amount"] for b in full["breakdown"] if b["key"] == "travel_to"] == [6000]


def test_plan_missing_fields(client):
    assert client.post("/api/plan", json={"destination": "Jaipur"}).status_code == 422


@pytest.mark.parametrize("city", ["Mumbai", "Kochi", "Leh", "Guwahati", "Port Blair", "Agartala", "Puducherry"])
def test_plan_works_for_other_regions(client, city):
    r = client.post("/api/plan", json={**PLAN_BODY, "destination": city, "interests": ["culture", "nature"]})
    assert r.status_code == 200 and r.json()["daily_plan"]


def test_plan_unknown_destination(client):
    assert client.post("/api/plan", json={**PLAN_BODY, "destination": "Atlantis"}).status_code == 404


def test_religious_places_alias_accepted(client):
    r = client.post("/api/plan", json={**PLAN_BODY, "destination": "Delhi", "interests": ["Religious places"]})
    assert r.status_code == 200 and r.json()["interests"] == ["religious"]


def _save_payload(client):
    plan = client.post("/api/plan", json=PLAN_BODY).json()
    return {"destination": plan["destination"], "days": plan["days"], "budget": plan["budget"],
            "travelers": plan["travelers"], "interests": plan["interests"], "itinerary": plan,
            "estimated_total_cost": plan["estimated_total_cost"]}


def test_trip_routes_require_login(client):
    payload = _save_payload(client)
    assert client.post("/api/trips/save", json=payload).status_code == 401
    assert client.get("/api/trips").status_code == 401
    assert client.get("/api/trips/" + "0" * 24).status_code == 401
    assert client.delete("/api/trips/" + "0" * 24).status_code == 401


def test_save_list_get_delete_trip(client, auth_headers):
    payload = _save_payload(client)
    saved = client.post("/api/trips/save", json=payload, headers=auth_headers)
    assert saved.status_code == 201
    trip_id = saved.json()["id"]

    listing = client.get("/api/trips", headers=auth_headers).json()
    assert [t["id"] for t in listing] == [trip_id] and "itinerary" not in listing[0]

    detail = client.get(f"/api/trips/{trip_id}", headers=auth_headers)
    assert detail.status_code == 200 and detail.json()["itinerary"]["daily_plan"]

    assert client.delete(f"/api/trips/{trip_id}", headers=auth_headers).status_code == 200
    assert client.get(f"/api/trips/{trip_id}", headers=auth_headers).status_code == 404
    assert client.get("/api/trips", headers=auth_headers).json() == []


def test_users_cannot_access_each_others_trips(client, auth_headers, other_headers):
    trip_id = client.post("/api/trips/save", json=_save_payload(client), headers=auth_headers).json()["id"]
    assert client.get("/api/trips", headers=other_headers).json() == []
    assert client.get(f"/api/trips/{trip_id}", headers=other_headers).status_code == 404
    assert client.delete(f"/api/trips/{trip_id}", headers=other_headers).status_code == 404
    # still there for the owner
    assert client.get(f"/api/trips/{trip_id}", headers=auth_headers).status_code == 200


def test_invalid_trip_id_is_404_not_500(client, auth_headers):
    assert client.get("/api/trips/not-an-id", headers=auth_headers).status_code == 404
    assert client.delete("/api/trips/not-an-id", headers=auth_headers).status_code == 404


def test_save_rejects_bad_payload(client, auth_headers):
    bad = {"destination": "Jaipur", "days": 3, "budget": 100, "travelers": 1, "interests": ["history"],
           "itinerary": {"no": "daily_plan"}, "estimated_total_cost": 0}
    assert client.post("/api/trips/save", json=bad, headers=auth_headers).status_code == 422

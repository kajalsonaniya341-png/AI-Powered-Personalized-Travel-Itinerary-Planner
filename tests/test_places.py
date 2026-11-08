"""Destination and place API tests."""


def test_destinations_list(client):
    r = client.get("/api/destinations")
    assert r.status_code == 200
    cities = {d["city"]: d for d in r.json()}
    assert {"Jaipur", "Delhi", "Bhopal", "Mumbai", "Kochi", "Leh", "Port Blair"} <= set(cities)
    assert len({d["state"] for d in r.json()}) == 36 and cities["Kochi"]["state"] == "Kerala"


def test_destination_detail_case_insensitive(client):
    r = client.get("/api/destinations/jaipur")
    assert r.status_code == 200 and r.json()["city"] == "Jaipur" and r.json()["place_count"] == 7
    assert client.get("/api/destinations/KOCHI").json()["places"][0]["state"] == "Kerala"


def test_destination_missing(client):
    assert client.get("/api/destinations/Atlantis").status_code == 404


def test_empty_database_gives_clear_404(client, fake_db):
    fake_db.places.docs.clear()
    r = client.get("/api/destinations")
    assert r.status_code == 404 and "seed" in r.json()["detail"].lower()


def test_all_places(client):
    r = client.get("/api/places")
    from tests.conftest import load_sample_places

    assert r.status_code == 200 and len(r.json()) == len(load_sample_places())


def test_places_by_city(client):
    r = client.get("/api/places/Delhi")
    assert r.status_code == 200 and len(r.json()) == 6
    assert all(p["city"] == "Delhi" for p in r.json())


def test_place_by_id(client):
    first = client.get("/api/places/Bhopal").json()[0]
    r = client.get(f"/api/places/{first['id']}")
    assert r.status_code == 200 and r.json()["name"] == first["name"]


def test_unknown_place_id_and_city(client):
    assert client.get("/api/places/" + "0" * 24).status_code == 404
    assert client.get("/api/places/Narnia").status_code == 404


def test_places_have_no_fake_ratings(client):
    assert all(p["rating"] is None and p["verified"] is False for p in client.get("/api/places").json())

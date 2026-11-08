"""ML layer: learned interest profiles from place text. Skipped when scikit-learn is missing."""
import pytest

pytest.importorskip("sklearn")

from app.services import ml  # noqa: E402
from app.services.itinerary import build_itinerary  # noqa: E402
from tests.conftest import load_sample_places  # noqa: E402


@pytest.fixture(scope="module")
def model():
    return ml.InterestModel(load_sample_places())


def test_model_learns_profiles_for_every_interest(model):
    assert {"history", "food", "religious", "wildlife"} <= set(model.profiles)
    assert model.n_places == len(load_sample_places())


def test_affinity_is_between_0_and_1_and_handles_unknown_interest(model):
    place = load_sample_places()[0]
    assert 0.0 <= model.affinity(place, ["history"]) <= 1.0
    assert model.affinity(place, ["skydiving"]) == 0.0


def test_text_alone_separates_interests_better_than_chance(model):
    places = load_sample_places()
    temple = next(p for p in places if p["name"] == "Lotus Temple")
    wildlife = next(p for p in places if "wildlife" in p["categories"])
    assert model.affinity(temple, ["religious"]) > model.affinity(temple, ["wildlife"])
    assert model.affinity(wildlife, ["wildlife"]) > model.affinity(wildlife, ["shopping"])


def test_blend_changes_score_but_keeps_rule_share():
    places = [dict(p, score=0.5) for p in load_sample_places() if p["city"] == "Jaipur"]
    m = ml.InterestModel(load_sample_places())
    assert ml.blend(places, m, ["history"]) is True
    assert all("ml_affinity" in p for p in places)
    assert all(0.4 - 1e-9 <= p["score"] <= 0.4 + ml.ML_WEIGHT + 1e-9 for p in places)


def test_blend_does_nothing_without_a_model():
    ranked = [{"name": "A", "score": 0.7}]
    assert ml.blend(ranked, None, ["history"]) is False and ranked[0]["score"] == 0.7


def test_itinerary_reports_ml_only_when_it_is_used():
    places = load_sample_places()
    jaipur = [p for p in places if p["city"] == "Jaipur"]
    plain = build_itinerary(jaipur, "Jaipur", 2, 20000, 2, ["history"], "budget")
    assert plain["algorithm"]["is_machine_learning"] is False
    mixed = build_itinerary(jaipur, "Jaipur", 2, 20000, 2, ["history"], "budget", ml_model=ml.InterestModel(places))
    algo = mixed["algorithm"]
    assert algo["is_machine_learning"] is True and algo["ml"]["weight"] == ml.ML_WEIGHT
    assert algo["ml"]["trained_on_places"] == len(places)
    names = [p["name"] for d in mixed["daily_plan"] for p in d["places"]]
    assert len(names) == len(set(names))

"""Small, honest machine-learning layer: learn what each interest "looks like" in the place text.

What it really is
    * TF-IDF turns every place (name + categories + description + city + state) into a vector.
    * For each interest (history, food, ...) the model LEARNS a profile: the average vector of all
      places in the dataset tagged with that interest (a nearest-centroid text classifier).
    * A place's ML affinity for the traveller = cosine similarity between the place and the profiles
      of the interests they picked. A place that is not tagged "history" but is described like one
      still gets a useful score.

What it is not
    * It is NOT trained on user behaviour (there is no user data yet) and it uses no external
      dataset. It learns only from the 349 sample places, whose descriptions are short, so the effect
      is deliberately limited: the ML score gets ML_WEIGHT (20%) of the final score and the
      rule-based score keeps 80%.
    * If scikit-learn is missing or anything fails, the app silently falls back to rules only.
"""
from typing import Optional

try:  # scikit-learn is optional at runtime
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    import numpy as np
    _AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when scikit-learn is not installed
    _AVAILABLE = False

ML_WEIGHT = 0.20
METHOD = "TF-IDF text vectors + learned interest profiles (nearest centroid, cosine similarity)"


def is_available() -> bool:
    return _AVAILABLE


def place_text(place: dict) -> str:
    """Text used to describe a place to the model. Category tags are left OUT on purpose,
    so the model learns from the wording and can be evaluated fairly against the tags."""
    return " ".join(str(place.get(k) or "") for k in ("name", "description", "city", "state"))


class InterestModel:
    """Fitted on a list of places; scores any place against any set of interests."""

    def __init__(self, places: list):
        self.n_places = len(places)
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        matrix = self.vectorizer.fit_transform([place_text(p) for p in places])
        self.profiles = {}
        categories = {c for p in places for c in p.get("categories", [])}
        for cat in sorted(categories):
            rows = [i for i, p in enumerate(places) if cat in p.get("categories", [])]
            if rows:
                centroid = np.asarray(matrix[rows].mean(axis=0))
                self.profiles[cat] = normalize(centroid)[0]

    def affinity(self, place: dict, interests: list) -> float:
        """0-1 similarity between a place's text and the learned profiles of the chosen interests."""
        vec = normalize(self.vectorizer.transform([place_text(place)]))
        sims = []
        for interest in interests:
            profile = self.profiles.get(interest)
            if profile is not None:
                sims.append(float(vec.dot(profile)[0]))
        return round(max(sims), 4) if sims else 0.0

    def affinities(self, places: list, interests: list) -> list:
        """Affinity for each place, rescaled so the best place in this list is 1.0."""
        raw = [self.affinity(p, interests) for p in places]
        top = max(raw) if raw else 0.0
        return [round(v / top, 4) if top > 0 else 0.0 for v in raw]


_cache = {"key": None, "model": None}


def get_model(db) -> Optional[InterestModel]:
    """Fit once per dataset size and cache. Returns None when ML cannot be used."""
    if not _AVAILABLE:
        return None
    try:
        places = list(db.places.find({}))
        key = len(places)
        if key < 20:
            return None
        if _cache["key"] != key:
            _cache["model"], _cache["key"] = InterestModel(places), key
        return _cache["model"]
    except Exception:
        return None


def blend(ranked: list, model: Optional[InterestModel], interests: list) -> bool:
    """Mix the ML affinity into each ranked place's score (in place). Returns True if ML was used."""
    if model is None or not interests or not ranked:
        return False
    for place, aff in zip(ranked, model.affinities(ranked, interests)):
        place["ml_affinity"] = aff
        place["score"] = round((1 - ML_WEIGHT) * place["score"] + ML_WEIGHT * aff, 4)
    ranked.sort(key=lambda p: (-p["score"], p["name"]))
    return True

"""Honest evaluation of the ML interest model with 5-fold cross-validation.

For every fold the model is fitted on 80% of the places and must rank the held-out 20% by how well
each place's TEXT (name, description, city, state - never its tags) matches an interest. We then
compare with the real tags using ROC-AUC (0.5 = random guessing, 1.0 = perfect).

Run:  python -m scripts.evaluate_ml
"""
import json
import random
from pathlib import Path

from app.services.ml import InterestModel, is_available

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if not is_available():
        print("scikit-learn is not installed: pip install -r requirements.txt")
        return 1
    from sklearn.metrics import roc_auc_score

    places = json.loads((ROOT / "data" / "places.json").read_text(encoding="utf-8"))["places"]
    rng = random.Random(42)
    order = list(range(len(places)))
    rng.shuffle(order)
    folds = [order[i::5] for i in range(5)]
    cats = sorted({c for p in places for c in p["categories"]})
    truth = {c: [] for c in cats}
    scores = {c: [] for c in cats}
    for fold in folds:
        held = set(fold)
        model = InterestModel([p for i, p in enumerate(places) if i not in held])
        for i in fold:
            for c in cats:
                truth[c].append(1 if c in places[i]["categories"] else 0)
                scores[c].append(model.affinity(places[i], [c]))
    print(f"{len(places)} places, 5-fold cross-validation, text only (tags hidden)\n")
    print(f"{'interest':<14}{'places':>7}{'ROC-AUC':>10}")
    aucs = []
    for c in cats:
        if 0 < sum(truth[c]) < len(truth[c]):
            auc = roc_auc_score(truth[c], scores[c])
            aucs.append(auc)
            print(f"{c:<14}{sum(truth[c]):>7}{auc:>10.2f}")
    print(f"\nmean ROC-AUC = {sum(aucs) / len(aucs):.2f}   (0.50 = random guessing)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

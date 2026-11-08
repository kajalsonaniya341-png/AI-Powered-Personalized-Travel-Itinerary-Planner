"""Destination routes. Destinations are derived from the cities present in MongoDB."""
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import place as place_model

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])


@router.get("")
def list_destinations(db=Depends(get_db)):
    cities = place_model.list_cities(db)
    if not cities:
        raise HTTPException(status_code=404,
                            detail="No destinations found. Run `python -m scripts.seed_database` to load the dataset.")
    return cities


@router.get("/{city}")
def get_destination(city: str, db=Depends(get_db)):
    canonical = place_model.match_city(db, city)
    if canonical is None:
        raise HTTPException(status_code=404, detail=f"Destination '{city}' is not supported yet.")
    places = place_model.find_places(db, canonical)
    categories = sorted({c for p in places for c in p["categories"]})
    return {"city": canonical, "place_count": len(places), "categories": categories, "places": places}

"""Place routes.

The spec lists GET /api/places/{city} and GET /api/places/{place_id}. Those two URLs
have the same shape, so to avoid duplicate routes there is ONE route,
/api/places/{identifier}: a 24-character hex string is treated as a place id, anything
else as a city name.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import place as place_model
from app.schemas.place import PlaceOut

router = APIRouter(prefix="/api/places", tags=["Places"])


@router.get("", response_model=list[PlaceOut])
def list_places(db=Depends(get_db)):
    return place_model.find_places(db)


@router.get("/{identifier}")
def get_places_or_place(identifier: str, db=Depends(get_db)):
    if place_model.is_object_id(identifier):
        found = place_model.find_place_by_id(db, identifier)
        if found is None:
            raise HTTPException(status_code=404, detail="Place not found.")
        return PlaceOut(**found)
    canonical = place_model.match_city(db, identifier)
    if canonical is None:
        raise HTTPException(status_code=404, detail=f"No places found for '{identifier}'.")
    return [PlaceOut(**p) for p in place_model.find_places(db, canonical)]

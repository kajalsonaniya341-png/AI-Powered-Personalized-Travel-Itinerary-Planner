"""Itinerary generation (public) and saved trips (login required, owner-only)."""
from fastapi import APIRouter, Depends, HTTPException

from app.database import get_db
from app.models import place as place_model
from app.models import trip as trip_model
from app.routers.auth import get_current_user
from app.schemas.itinerary import PlanRequest, SaveTripRequest
from app.services import ml
from app.services.itinerary import NoPlacesError, build_itinerary

router = APIRouter(prefix="/api", tags=["Itinerary and Trips"])


@router.post("/plan")
def plan_trip(body: PlanRequest, db=Depends(get_db)):
    """Generate a personalised itinerary from the places stored in MongoDB."""
    city = place_model.match_city(db, body.destination)
    if city is None:
        raise HTTPException(status_code=404, detail=f"Destination '{body.destination}' is not supported yet.")
    places = place_model.find_places(db, city)
    try:
        return build_itinerary(places, city, body.days, body.budget, body.travelers,
                               body.interests, body.travel_style, body.nights, body.travel_cost_per_person, body.travel_mode,
                               ml_model=ml.get_model(db))
    except NoPlacesError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/trips")
def my_trips(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    return trip_model.list_trips(db, str(current_user["_id"]))


@router.post("/trips/save", status_code=201)
def save_trip(body: SaveTripRequest, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    doc = trip_model.create_trip(db, str(current_user["_id"]), body.model_dump())
    return trip_model.serialize_trip(doc, include_itinerary=False)


@router.get("/trips/{trip_id}")
def get_trip(trip_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    trip = trip_model.get_trip(db, str(current_user["_id"]), trip_id)
    if trip is None:  # also returned for other users' trips, so existence is not revealed
        raise HTTPException(status_code=404, detail="Trip not found.")
    return trip


@router.delete("/trips/{trip_id}")
def delete_trip(trip_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    if not trip_model.delete_trip(db, str(current_user["_id"]), trip_id):
        raise HTTPException(status_code=404, detail="Trip not found.")
    return {"message": "Trip deleted."}

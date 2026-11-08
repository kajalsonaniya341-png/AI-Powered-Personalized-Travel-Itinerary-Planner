"""Response shape for a tourist attraction."""
from pydantic import BaseModel


class PlaceOut(BaseModel):
    id: str
    name: str
    city: str
    state: str | None = None
    categories: list[str]
    description: str
    cost: float | None = None
    cost_is_estimate: bool = True
    hours: float | None = None
    hours_is_estimate: bool = True
    rating: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    coordinates_approximate: bool = False
    source: str
    verified: bool

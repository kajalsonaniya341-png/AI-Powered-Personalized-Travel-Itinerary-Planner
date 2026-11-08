"""Request shapes for itinerary planning and saving trips."""
import json
from typing import Any

from pydantic import BaseModel, Field, field_validator

ALLOWED_INTERESTS = {
    "history", "adventure", "nature", "food", "culture",
    "shopping", "religious", "museums", "wildlife",
}
INTEREST_ALIASES = {"religious places": "religious", "religious_places": "religious", "museum": "museums"}
TRAVEL_STYLES = {"budget", "balanced", "luxury"}
TRAVEL_MODES = {"none", "flight", "train", "bus", "car"}


class PlanRequest(BaseModel):
    destination: str = Field(min_length=1, max_length=60)
    days: int = Field(ge=1, le=7, description="Trip length in days (1-7)")
    budget: float = Field(gt=0, le=10_000_000, description="Total trip budget in INR")
    travelers: int = Field(ge=1, le=20)
    interests: list[str] = Field(min_length=1, max_length=9)
    travel_style: str = "balanced"
    nights: int | None = Field(default=None, ge=0, le=14, description="Nights of stay (default: days - 1)")
    travel_cost_per_person: float = Field(default=0, ge=0, le=1_000_000, description="Round-trip travel to the destination, per person, INR")
    travel_mode: str = "none"

    @field_validator("interests")
    @classmethod
    def clean_interests(cls, values):
        cleaned = []
        for v in values:
            key = INTEREST_ALIASES.get(v.strip().lower(), v.strip().lower())
            if key not in ALLOWED_INTERESTS:
                raise ValueError(f"Unknown interest '{v}'. Allowed: {sorted(ALLOWED_INTERESTS)}")
            if key not in cleaned:
                cleaned.append(key)
        return cleaned

    @field_validator("travel_mode")
    @classmethod
    def clean_mode(cls, v):
        v = v.strip().lower()
        if v not in TRAVEL_MODES:
            raise ValueError(f"travel_mode must be one of {sorted(TRAVEL_MODES)}")
        return v

    @field_validator("travel_style")
    @classmethod
    def clean_style(cls, v):
        v = v.strip().lower()
        if v not in TRAVEL_STYLES:
            raise ValueError(f"travel_style must be one of {sorted(TRAVEL_STYLES)}")
        return v


class SaveTripRequest(BaseModel):
    destination: str = Field(min_length=1, max_length=60)
    days: int = Field(ge=1, le=7)
    budget: float = Field(gt=0, le=10_000_000)
    travelers: int = Field(ge=1, le=20)
    interests: list[str] = Field(min_length=1, max_length=9)
    itinerary: dict[str, Any]
    estimated_total_cost: float = Field(ge=0)

    @field_validator("itinerary")
    @classmethod
    def itinerary_not_huge(cls, v):
        if len(json.dumps(v)) > 200_000:
            raise ValueError("Itinerary is too large to save.")
        if "daily_plan" not in v:
            raise ValueError("Itinerary must contain 'daily_plan'.")
        return v

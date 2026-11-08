"""Request shapes for the AI endpoints."""
import json
from typing import Any

from pydantic import BaseModel, Field, field_validator


class _WithItinerary(BaseModel):
    itinerary: dict[str, Any]

    @field_validator("itinerary")
    @classmethod
    def valid_itinerary(cls, v):
        if "daily_plan" not in v or not isinstance(v["daily_plan"], list):
            raise ValueError("Itinerary must contain 'daily_plan'.")
        if len(json.dumps(v)) > 300_000:
            raise ValueError("Itinerary is too large.")
        return v


class InsightsRequest(_WithItinerary):
    pass


class AskRequest(_WithItinerary):
    question: str = Field(min_length=3, max_length=300)

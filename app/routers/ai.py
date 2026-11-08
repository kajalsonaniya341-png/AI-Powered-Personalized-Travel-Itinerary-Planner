"""AI endpoints. They are public (like /api/plan) but rate-limited, and report clearly when AI is off."""
from fastapi import APIRouter, HTTPException, Request

from app.schemas.ai import AskRequest, InsightsRequest
from app.services import ai

router = APIRouter(prefix="/api/ai", tags=["AI"])


def _guard(request: Request) -> None:
    if not ai.is_enabled():
        raise HTTPException(status_code=503, detail="AI features are not enabled on this server.")
    client = request.client.host if request.client else "unknown"
    if not ai.check_rate_limit(client):
        raise HTTPException(status_code=429, detail="Too many AI requests. Please wait a minute and try again.")


@router.get("/status")
def status():
    return {"enabled": ai.is_enabled(), "provider": ai.config.AI_PROVIDER if ai.is_enabled() else None,
            "model": ai.model_name() if ai.is_enabled() else None}


@router.post("/insights")
def insights(body: InsightsRequest, request: Request):
    _guard(request)
    try:
        return ai.generate_insights(body.itinerary)
    except ai.AIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.post("/ask")
def ask(body: AskRequest, request: Request):
    _guard(request)
    try:
        return {"answer": ai.answer_question(body.itinerary, body.question)}
    except ai.AIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

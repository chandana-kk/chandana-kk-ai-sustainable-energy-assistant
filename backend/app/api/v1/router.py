"""API v1 router aggregation."""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.v1 import admin, alerts, auth, energy, iot, predictions, recommendations, settings

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(energy.router)
api_router.include_router(predictions.router)
api_router.include_router(recommendations.router)
api_router.include_router(alerts.router)
api_router.include_router(settings.router)
api_router.include_router(iot.router)
api_router.include_router(admin.router)


@api_router.get("/auth/me")
async def auth_me(user: dict = Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "full_name": user.get("full_name"),
        "role": user.get("role", "user"),
        "preferred_language": user.get("preferred_language", "en"),
        "theme": user.get("theme", "dark"),
    }

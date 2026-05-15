from fastapi import APIRouter

from app.api.v1 import admin, alerts, auth, energy, iot, predictions, recommendations, settings

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(energy.router)
api_router.include_router(predictions.router)
api_router.include_router(recommendations.router)
api_router.include_router(alerts.router)
api_router.include_router(settings.router)
api_router.include_router(admin.router)
api_router.include_router(iot.router)

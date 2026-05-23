"""AI prediction endpoints."""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.services.ml_service import ml_service

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get("/{horizon}")
async def get_predictions(horizon: str = "24h", user: dict = Depends(get_current_user)):
    if horizon not in ("24h", "7d", "peak"):
        horizon = "24h"
    points = ml_service.predict_usage(user["id"], horizon)
    peak = max(points, key=lambda p: p["predicted_kwh"]) if points else None
    return {
        "horizon": horizon,
        "predictions": points,
        "peak_prediction": peak,
        "model": "LSTM" if horizon != "peak" else "heuristic",
    }


@router.get("/cost-estimate")
async def cost_estimate(user: dict = Depends(get_current_user)):
    from app.core.config import get_settings
    from app.services.energy_simulator import get_simulator

    reading = get_simulator(user["id"]).next_reading()
    settings = get_settings()
    preds = ml_service.predict_usage(user["id"], "24h")
    forecast_kwh = sum(p["predicted_kwh"] for p in preds[:24])
    return {
        "current_monthly_bill": reading["estimated_bill"],
        "forecast_daily_kwh": round(forecast_kwh, 2),
        "forecast_daily_cost": round(forecast_kwh * settings.tariff_per_kwh, 2),
        "tariff_per_kwh": settings.tariff_per_kwh,
    }

"""Energy monitoring and history APIs."""
from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user
from app.core.database import get_database
from app.services.energy_simulator import get_simulator

router = APIRouter(prefix="/energy", tags=["Energy"])


@router.get("/live")
async def live_energy(user: dict = Depends(get_current_user)):
    reading = get_simulator(user["id"]).next_reading()
    return reading


@router.get("/history")
async def energy_history(
    period: str = Query("daily", pattern="^(daily|weekly|monthly)$"),
    user: dict = Depends(get_current_user),
):
    return get_simulator(user["id"]).history(period)


@router.get("/peak-analysis")
async def peak_analysis(user: dict = Depends(get_current_user)):
    history = get_simulator(user["id"]).history("daily")
    peak = max(history, key=lambda x: x["kwh"])
    return {
        "peak_label": peak["label"],
        "peak_kwh": peak["kwh"],
        "peak_cost": peak["cost"],
        "off_peak_hours": ["00:00-06:00", "22:00-24:00"],
        "recommendation": "Schedule heavy loads outside peak window.",
    }


@router.get("/savings-tips")
async def savings_tips():
    return [
        {"tip": "Use LED bulbs", "savings_percent": 80},
        {"tip": "Set AC to 26°C", "savings_percent": 18},
        {"tip": "Unplug standby devices", "savings_percent": 10},
        {"tip": "Use natural light during day", "savings_percent": 15},
        {"tip": "Run washing machine off-peak", "savings_percent": 12},
    ]


@router.post("/readings/store")
async def store_reading(user: dict = Depends(get_current_user)):
    """Persist a snapshot for historical analytics."""
    db = get_database()
    reading = get_simulator(user["id"]).next_reading()
    await db.energy_readings.insert_one({**reading, "user_id": user["id"]})
    return {"stored": True}

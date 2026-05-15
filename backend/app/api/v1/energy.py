from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.database import get_database
from app.schemas.energy import DashboardHistory, EnergySnapshot
from app.services.energy_simulator import simulator
from app.services.ml_service import generate_history

router = APIRouter(prefix="/energy", tags=["Energy"])


async def _build_snapshot(user: dict) -> dict:
    live = simulator.generate_live_reading()
    agg = simulator.aggregate_usage(live["power_kw"])
    appliances = simulator.estimate_appliances(live["power_kw"])
    return {"live": live, "appliances": appliances, **agg}


@router.get("/live", response_model=EnergySnapshot)
async def get_live_energy(user: dict = Depends(get_current_user)):
    snap = await _build_snapshot(user)
    db = get_database()
    await db.energy_readings.insert_one({
        "user_id": user["id"],
        **snap,
        "recorded_at": datetime.now(timezone.utc),
    })
    return EnergySnapshot(
        live=snap["live"],
        daily_kwh=snap["daily_kwh"],
        weekly_kwh=snap["weekly_kwh"],
        monthly_kwh=snap["monthly_kwh"],
        estimated_bill=snap["estimated_bill"],
        carbon_kg=snap["carbon_kg"],
        appliances=snap["appliances"],
        peak_hour=snap["peak_hour"],
        savings_potential=snap["savings_potential"],
    )


@router.get("/history", response_model=DashboardHistory)
async def get_history(user: dict = Depends(get_current_user)):
    return generate_history()

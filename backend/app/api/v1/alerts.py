from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.database import get_database
from app.schemas.energy import AlertItem
from app.services.alert_service import default_tips, evaluate_alerts
from app.api.v1.energy import _build_snapshot
from datetime import datetime, timezone

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=list[AlertItem])
async def get_alerts(user: dict = Depends(get_current_user)):
    snap = await _build_snapshot(user)
    alerts = evaluate_alerts(user, snap)
    db = get_database()
    for a in alerts:
        a["user_id"] = user["id"]
        await db.alerts.insert_one(a)
    return [AlertItem(**a) for a in alerts]


@router.get("/tips")
async def get_tips(user: dict = Depends(get_current_user)):
    return {"tips": default_tips()}


@router.patch("/{alert_id}/read")
async def mark_read(alert_id: str, user: dict = Depends(get_current_user)):
    db = get_database()
    await db.alerts.update_one(
        {"id": alert_id, "user_id": user["id"]},
        {"$set": {"read": True}},
    )
    return {"ok": True}

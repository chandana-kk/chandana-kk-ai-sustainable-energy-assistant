"""Alerts and notifications API."""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.database import get_database
from app.services.alert_service import get_user_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("")
async def list_alerts(user: dict = Depends(get_current_user)):
    return {"alerts": await get_user_alerts(user["id"])}


@router.patch("/{alert_id}/read")
async def mark_read(alert_id: str, user: dict = Depends(get_current_user)):
    db = get_database()
    await db.alerts.update_one(
        {"_id": alert_id, "user_id": user["id"]},
        {"$set": {"read": True}},
    )
    return {"ok": True}

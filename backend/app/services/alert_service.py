"""Intelligent alerts based on simulated readings and thresholds."""
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from app.core.config import get_settings
from app.core.database import get_database
from app.services.energy_simulator import get_simulator


async def evaluate_and_store_alerts(user_id: str) -> List[dict]:
    """Check current reading against rules; persist new alerts."""
    reading = get_simulator(user_id).next_reading()
    settings = get_settings()
    db = get_database()
    new_alerts = []

    if reading["power_kw"] > 2.5:
        new_alerts.append({
            "type": "high_usage",
            "severity": "warning",
            "message": f"High energy usage detected: {reading['power_kw']:.2f} kW",
        })
    if reading["power_kw"] > 3.5:
        new_alerts.append({
            "type": "power_spike",
            "severity": "critical",
            "message": "Abnormal power spike detected. Check for faulty appliances.",
        })
    if reading["estimated_bill"] > settings.bill_alert_threshold:
        new_alerts.append({
            "type": "bill_threshold",
            "severity": "warning",
            "message": f"Estimated bill ₹{reading['estimated_bill']:.0f} exceeds threshold.",
        })

    stored = []
    for a in new_alerts:
        doc = {
            "_id": str(uuid4()),
            "user_id": user_id,
            "type": a["type"],
            "severity": a["severity"],
            "message": a["message"],
            "created_at": datetime.now(timezone.utc),
            "read": False,
        }
        await db.alerts.update_one(
            {"_id": doc["_id"]},
            {"$set": doc},
            upsert=True,
        )
        stored.append({
            "id": doc["_id"],
            "type": doc["type"],
            "severity": doc["severity"],
            "message": doc["message"],
            "created_at": doc["created_at"].isoformat(),
            "read": doc["read"],
        })

    return stored


async def get_user_alerts(user_id: str, limit: int = 20) -> List[dict]:
    db = get_database()
    await evaluate_and_store_alerts(user_id)
    cursor = db.alerts.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
    alerts = []
    async for doc in cursor:
        alerts.append({
            "id": doc.get("_id", str(doc.get("id", ""))),
            "type": doc["type"],
            "severity": doc["severity"],
            "message": doc["message"],
            "created_at": doc["created_at"].isoformat()
            if hasattr(doc["created_at"], "isoformat")
            else str(doc["created_at"]),
            "read": doc.get("read", False),
        })
    return alerts

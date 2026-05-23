"""IoT / MQTT placeholder endpoints for future ESP32 + SCT-013 integration."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.core.database import get_database
from app.schemas.energy import IoTReading

router = APIRouter(prefix="/iot", tags=["IoT"])


@router.get("/status")
async def iot_status():
    settings = get_settings()
    return {
        "mqtt_enabled": settings.mqtt_enabled,
        "mqtt_broker": f"{settings.mqtt_broker_host}:{settings.mqtt_broker_port}",
        "mqtt_topic": settings.mqtt_topic_energy,
        "hardware_connected": False,
        "mode": "simulation",
        "note": "Set MQTT_ENABLED=true and connect ESP32 when hardware is ready.",
    }


@router.post("/readings")
async def ingest_reading(
    data: IoTReading,
    user: dict = Depends(get_current_user),
):
    """Accept sensor readings from ESP32; stored for analytics."""
    db = get_database()
    doc = {
        **data.model_dump(),
        "user_id": user["id"],
        "received_at": datetime.now(timezone.utc),
        "source": "esp32",
    }
    if doc.get("timestamp") is None:
        doc["timestamp"] = doc["received_at"]
    await db.iot_readings.insert_one(doc)
    return {"accepted": True, "device_id": data.device_id}


@router.post("/mqtt/placeholder")
async def mqtt_placeholder():
  return {
      "message": "MQTT subscriber not started. Enable MQTT_ENABLED in .env for production.",
  }

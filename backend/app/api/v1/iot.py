"""IoT placeholders for future ESP32 + SCT-013 via MQTT."""

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.config import get_settings

router = APIRouter(prefix="/iot", tags=["IoT"])


@router.get("/mqtt/status")
async def mqtt_status(user: dict = Depends(get_current_user)):
    settings = get_settings()
    return {
        "enabled": settings.mqtt_enabled,
        "broker": f"{settings.mqtt_broker_host}:{settings.mqtt_broker_port}",
        "topic": settings.mqtt_topic_energy,
        "message": "Connect ESP32 firmware to publish readings to MQTT topic.",
    }


@router.post("/readings")
async def ingest_hardware_reading(payload: dict, user: dict = Depends(get_current_user)):
    """Endpoint for future hardware to POST real sensor data."""
    return {
        "status": "accepted",
        "user_id": user["id"],
        "received": payload,
        "note": "Hardware integration placeholder — wire ESP32 here.",
    }

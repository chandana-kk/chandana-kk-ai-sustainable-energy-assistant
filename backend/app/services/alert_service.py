"""Intelligent alerts for usage spikes and bill thresholds."""

from datetime import datetime, timezone
from uuid import uuid4

from app.core.config import get_settings
from app.services.energy_simulator import simulator


def evaluate_alerts(user: dict, snapshot: dict) -> list[dict]:
    settings = get_settings()
    alerts = []
    live = snapshot.get("live", {})
    power_kw = live.get("power_kw", 0)
    bill = snapshot.get("estimated_bill", 0)
    threshold = user.get("bill_threshold", settings.bill_alert_threshold)

    if power_kw > 4.5:
        alerts.append(_alert(
            "high_usage",
            f"High energy usage detected: {power_kw:.2f} kW. Consider turning off non-essential devices.",
            "warning",
        ))
    if power_kw > 5.5:
        alerts.append(_alert(
            "power_spike",
            f"Abnormal power spike: {power_kw:.2f} kW. Check for faulty appliances or short circuits.",
            "critical",
        ))
    if bill > threshold:
        alerts.append(_alert(
            "bill_threshold",
            f"Estimated monthly bill ₹{bill:.0f} exceeds your threshold of ₹{threshold:.0f}.",
            "warning",
        ))
    hour = datetime.now().hour
    if 18 <= hour <= 22 and power_kw > 3.5:
        alerts.append(_alert(
            "peak_period",
            "Peak tariff period active. Defer heavy loads to save up to 40% on those units.",
            "info",
        ))
    return alerts


def _alert(alert_type: str, message: str, severity: str) -> dict:
    return {
        "id": str(uuid4()),
        "type": alert_type,
        "message": message,
        "severity": severity,
        "created_at": datetime.now(timezone.utc),
        "read": False,
    }


def default_tips() -> list[str]:
    return [
        "Unplug chargers when not in use to eliminate phantom loads.",
        "Use natural light during daytime to reduce lighting consumption.",
        "Set refrigerator temperature to 3-4°C for optimal efficiency.",
        "Batch cooking reduces oven preheat cycles and saves energy.",
        "Enable eco mode on AC during moderate weather conditions.",
    ]

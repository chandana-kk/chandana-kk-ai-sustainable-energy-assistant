"""Simulated real-time electricity readings and appliance usage."""

import math
import random
from datetime import datetime, timezone

from app.core.config import get_settings

APPLIANCE_PROFILES = [
    {"name": "Air Conditioner", "category": "hvac", "base_w": 1800, "variance": 400},
    {"name": "Refrigerator", "category": "kitchen", "base_w": 150, "variance": 30},
    {"name": "Washing Machine", "category": "laundry", "base_w": 500, "variance": 200},
    {"name": "TV & Entertainment", "category": "entertainment", "base_w": 120, "variance": 40},
    {"name": "Lighting", "category": "lighting", "base_w": 200, "variance": 80},
    {"name": "Standby Loads", "category": "standby", "base_w": 85, "variance": 25},
]


class EnergySimulator:
    def __init__(self) -> None:
        self._tick = 0

    def generate_live_reading(self) -> dict:
        self._tick += 1
        hour = datetime.now().hour
        # Peak hours 18-22
        peak_factor = 1.35 if 18 <= hour <= 22 else (0.75 if 2 <= hour <= 6 else 1.0)
        noise = math.sin(self._tick / 8) * 0.15 + random.uniform(-0.08, 0.08)
        base_power = 2.2 * peak_factor * (1 + noise)
        voltage = round(220 + random.uniform(-5, 5), 1)
        power_w = max(200, base_power * 1000)
        current = round(power_w / voltage, 2)
        return {
            "voltage": voltage,
            "current": current,
            "power_kw": round(power_w / 1000, 3),
            "power_factor": round(random.uniform(0.88, 0.98), 2),
            "frequency": round(49.8 + random.uniform(-0.2, 0.2), 1),
            "timestamp": datetime.now(timezone.utc),
        }

    def estimate_appliances(self, total_power_w: float) -> list[dict]:
        """NILM-style dummy disaggregation based on weighted profiles."""
        weights = []
        for profile in APPLIANCE_PROFILES:
            w = profile["base_w"] + random.uniform(-profile["variance"], profile["variance"])
            weights.append(max(10, w))
        total_w = sum(weights)
        scale = (total_power_w * 1000) / total_w if total_w else 1
        appliances = []
        for profile, w in zip(APPLIANCE_PROFILES, weights):
            power = w * scale
            share = (power / (total_power_w * 1000)) * 100 if total_power_w else 0
            appliances.append({
                "name": profile["name"],
                "power_w": round(power, 1),
                "share_percent": round(share, 1),
                "category": profile["category"],
            })
        return sorted(appliances, key=lambda x: x["power_w"], reverse=True)

    def aggregate_usage(self, live_power_kw: float) -> dict:
        settings = get_settings()
        hour = datetime.now().hour
        daily_base = 12 + (live_power_kw * 4)
        weekly = daily_base * 6.8
        monthly = daily_base * 28
        rate = settings.electricity_rate_per_kwh
        if 18 <= hour <= 22:
            rate *= settings.peak_rate_multiplier
        bill = monthly * rate
        carbon = monthly * 0.82  # kg CO2 per kWh (India grid avg approx)
        return {
            "daily_kwh": round(daily_base, 2),
            "weekly_kwh": round(weekly, 2),
            "monthly_kwh": round(monthly, 2),
            "estimated_bill": round(bill, 2),
            "carbon_kg": round(carbon, 2),
            "peak_hour": "18:00 - 22:00",
            "savings_potential": round(bill * 0.18, 2),
        }


simulator = EnergySimulator()

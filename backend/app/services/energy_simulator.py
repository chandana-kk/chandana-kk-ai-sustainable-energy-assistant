"""Simulated real-time electricity readings for demo without hardware."""
import math
import random
from datetime import datetime, timezone
from typing import Dict

from app.core.config import get_settings


class EnergySimulator:
    """Generates realistic fluctuating power readings and appliance breakdown."""

    APPLIANCE_PROFILES = {
        "ac": (0.8, 2.2),
        "refrigerator": (0.15, 0.25),
        "tv": (0.05, 0.15),
        "washing_machine": (0.0, 1.8),
        "lights": (0.08, 0.35),
        "fan": (0.05, 0.12),
        "microwave": (0.0, 1.2),
        "computer": (0.1, 0.4),
        "water_heater": (0.0, 2.5),
        "standby": (0.02, 0.08),
    }

    def __init__(self, user_id: str):
        self.user_id = user_id
        self._tick = 0
        self._daily_kwh = random.uniform(8.0, 14.0)
        self._monthly_kwh = random.uniform(220.0, 380.0)

    def next_reading(self) -> dict:
        self._tick += 1
        settings = get_settings()
        t = datetime.now(timezone.utc)
        hour = t.hour

        # Diurnal pattern: higher evening usage
        base_load = 0.4 + 0.35 * math.sin((hour - 6) * math.pi / 12)
        noise = random.uniform(-0.08, 0.08)
        power_kw = max(0.15, base_load + noise + random.uniform(0, 0.5))

        voltage = random.uniform(228, 242)
        current = (power_kw * 1000) / (voltage * 0.92)
        power_w = power_kw * 1000

        # Increment cumulative usage slightly each tick
        increment = power_kw * (settings.energy_sim_interval_seconds / 3600)
        self._daily_kwh += increment
        self._monthly_kwh += increment

        appliances = self._estimate_appliances(power_kw)
        estimated_bill = self._monthly_kwh * settings.tariff_per_kwh
        carbon_kg = self._monthly_kwh * 0.82  # kg CO2 per kWh (India grid avg)

        return {
            "timestamp": t.isoformat(),
            "voltage": round(voltage, 1),
            "current": round(current, 2),
            "power_kw": round(power_kw, 3),
            "power_w": round(power_w, 0),
            "frequency": round(random.uniform(49.8, 50.2), 2),
            "power_factor": round(random.uniform(0.88, 0.98), 2),
            "daily_kwh": round(self._daily_kwh, 2),
            "monthly_kwh": round(self._monthly_kwh, 2),
            "estimated_bill": round(estimated_bill, 2),
            "carbon_kg": round(carbon_kg, 2),
            "appliances": appliances,
            "user_id": self.user_id,
        }

    def _estimate_appliances(self, total_kw: float) -> Dict[str, float]:
        """NILM-style dummy disaggregation: allocate total power to appliances."""
        active = []
        for name, (lo, hi) in self.APPLIANCE_PROFILES.items():
            if random.random() > 0.35:
                share = random.uniform(lo, hi)
                active.append((name, share))

        if not active:
            return {"standby": round(total_kw, 3)}

        total_share = sum(s for _, s in active) or 1.0
        scale = total_kw / total_share
        return {name: round(share * scale, 3) for name, share in active}

    def history(self, period: str = "daily") -> list:
        """Generate chart history for daily / weekly / monthly views."""
        settings = get_settings()
        if period == "weekly":
            labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            base = [10, 12, 11, 13, 14, 16, 15]
        elif period == "monthly":
            labels = [f"W{i}" for i in range(1, 5)]
            base = [68, 72, 75, 70]
        else:
            labels = [f"{h:02d}:00" for h in range(0, 24, 2)]
            base = [
                0.3, 0.25, 0.2, 0.2, 0.25, 0.4, 0.8, 1.2,
                1.0, 0.9, 0.85, 1.1, 1.3, 1.2, 1.0, 0.95,
                1.1, 1.5, 2.0, 2.2, 2.0, 1.6, 1.0, 0.5,
            ]
        return [
            {
                "label": lbl,
                "kwh": round(kwh + random.uniform(-0.5, 0.5), 2),
                "cost": round((kwh + random.uniform(-0.5, 0.5)) * settings.tariff_per_kwh, 2),
            }
            for lbl, kwh in zip(labels, base)
        ]


# Per-user simulator instances
_simulators: Dict[str, EnergySimulator] = {}


def get_simulator(user_id: str) -> EnergySimulator:
    if user_id not in _simulators:
        _simulators[user_id] = EnergySimulator(user_id)
    return _simulators[user_id]

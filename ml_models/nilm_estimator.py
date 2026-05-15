"""Dummy NILM (Non-Intrusive Load Monitoring) appliance disaggregation."""

import numpy as np
from typing import List, Dict


APPLIANCE_SIGNATURES = {
    "ac": {"freq_hz": 50, "power_range": (800, 2500), "duty_cycle": 0.7},
    "fridge": {"freq_hz": 50, "power_range": (80, 200), "duty_cycle": 0.4},
    "washing_machine": {"freq_hz": 50, "power_range": (200, 800), "duty_cycle": 0.2},
}


def disaggregate(total_power_w: float, duration_minutes: int = 60) -> List[Dict]:
    """
    Estimate appliance contributions from aggregate power (demo logic).
    Real NILM uses edge detection, harmonic analysis, and trained classifiers.
    """
    profiles = [
        ("Air Conditioner", 0.35),
        ("Refrigerator", 0.12),
        ("Washing Machine", 0.15),
        ("TV & Entertainment", 0.10),
        ("Lighting", 0.18),
        ("Standby Loads", 0.10),
    ]
    results = []
    for name, share in profiles:
        power = total_power_w * share * np.random.uniform(0.9, 1.1)
        results.append({
            "name": name,
            "power_w": round(power, 1),
            "share_percent": round(share * 100, 1),
        })
    return sorted(results, key=lambda x: x["power_w"], reverse=True)

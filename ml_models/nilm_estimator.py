"""NILM-style appliance disaggregation (heuristic demo)."""
from typing import Dict, List


APPLIANCE_SIGNATURES = {
    "ac": {"min_kw": 0.8, "max_kw": 2.5, "duty": 0.6},
    "refrigerator": {"min_kw": 0.1, "max_kw": 0.3, "duty": 0.9},
    "tv": {"min_kw": 0.05, "max_kw": 0.2, "duty": 0.5},
    "washing_machine": {"min_kw": 0.0, "max_kw": 2.0, "duty": 0.15},
    "lights": {"min_kw": 0.05, "max_kw": 0.4, "duty": 0.7},
    "water_heater": {"min_kw": 0.0, "max_kw": 2.5, "duty": 0.2},
}


def disaggregate(total_kw: float, active_appliances: List[str] | None = None) -> Dict[str, float]:
    """
    Dummy NILM: distribute total power across known appliance signatures.
    Replace with CNN/Seq2Seq model when labeled data is available.
    """
    import random

    apps = active_appliances or list(APPLIANCE_SIGNATURES.keys())
    random.shuffle(apps)
    result = {}
    remaining = total_kw
    for name in apps[:5]:
        sig = APPLIANCE_SIGNATURES.get(name, {"min_kw": 0.05, "max_kw": 0.2})
        if random.random() > sig.get("duty", 0.5):
            continue
        load = random.uniform(sig["min_kw"], min(sig["max_kw"], remaining))
        result[name] = round(load, 3)
        remaining -= load
        if remaining <= 0.05:
            break
    if remaining > 0:
        result["other"] = round(remaining, 3)
    return result


if __name__ == "__main__":
    print(disaggregate(2.1))

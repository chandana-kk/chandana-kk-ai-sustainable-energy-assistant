"""ML inference: LSTM predictions, XGBoost recommendations, NILM estimates."""
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

import numpy as np

from app.core.config import get_settings
from app.services.energy_simulator import get_simulator


def _models_dir() -> Path:
    settings = get_settings()
    base = Path(__file__).resolve().parents[3] / "ml_models" / "saved_models"
    if not base.exists():
        alt = Path(settings.ml_models_path)
        if alt.is_absolute():
            return alt
        return Path(__file__).resolve().parents[2] / alt
    return base


class MLService:
    """Loads trained models when available; falls back to heuristic logic."""

    def predict_usage(self, user_id: str, horizon: str = "24h") -> List[dict]:
        hours = 24 if horizon == "24h" else (168 if horizon == "7d" else 24)
        sim = get_simulator(user_id)
        reading = sim.next_reading()
        base = reading["power_kw"]

        lstm_path = _models_dir() / "lstm_model.h5"
        if lstm_path.exists():
            try:
                return self._lstm_predict(base, hours)
            except Exception:
                pass

        return self._heuristic_predict(base, hours)

    def _heuristic_predict(self, base_kw: float, hours: int) -> List[dict]:
        import math
        import random

        now = datetime.now(timezone.utc)
        points = []
        for i in range(min(hours, 48)):
            t = now + timedelta(hours=i)
            h = t.hour
            factor = 0.5 + 0.5 * math.sin((h - 6) * math.pi / 12)
            kwh = max(0.1, base_kw * factor * random.uniform(0.85, 1.15))
            points.append({
                "hour": t.strftime("%H:%M"),
                "predicted_kwh": round(kwh, 3),
                "confidence": round(random.uniform(0.78, 0.95), 2),
            })
        return points

    def _lstm_predict(self, base_kw: float, hours: int) -> List[dict]:
        from tensorflow import keras

        model = keras.models.load_model(_models_dir() / "lstm_model.h5")
        seq = np.array([[base_kw] * 24]).reshape(1, 24, 1)
        preds = model.predict(seq, verbose=0)[0]
        now = datetime.now(timezone.utc)
        return [
            {
                "hour": (now + timedelta(hours=i)).strftime("%H:%M"),
                "predicted_kwh": round(float(preds[i % len(preds)]), 3),
                "confidence": 0.88,
            }
            for i in range(min(hours, len(preds)))
        ]

    def get_recommendations(self, user_id: str) -> List[dict]:
        sim = get_simulator(user_id)
        reading = sim.next_reading()
        model_path = _models_dir() / "optimizer_model.joblib"

        if model_path.exists():
            try:
                import joblib
                clf = joblib.load(model_path)
                features = np.array([[
                    reading["power_kw"],
                    reading["daily_kwh"],
                    reading["monthly_kwh"],
                    reading["estimated_bill"],
                ]])
                score = float(clf.predict(features)[0])
            except Exception:
                score = reading["power_kw"]
        else:
            score = reading["power_kw"]

        recs = []
        if reading["power_kw"] > 1.5:
            recs.append({
                "id": "r1",
                "title": "Reduce AC load",
                "description": "Set AC to 26°C instead of 22°C to save 15–20% cooling energy.",
                "priority": "high",
                "potential_savings_inr": 450,
                "category": "hvac",
            })
        if reading["appliances"].get("standby", 0) > 0.05:
            recs.append({
                "id": "r2",
                "title": "Eliminate standby power",
                "description": "Unplug idle chargers and switch off TV/set-top box at night.",
                "priority": "medium",
                "potential_savings_inr": 120,
                "category": "standby",
            })
        hour = datetime.now().hour
        if 18 <= hour <= 22:
            recs.append({
                "id": "r3",
                "title": "Shift to off-peak hours",
                "description": "Run washing machine and water heater after 10 PM for lower tariffs.",
                "priority": "medium",
                "potential_savings_inr": 200,
                "category": "scheduling",
            })
        recs.append({
            "id": "r4",
            "title": "LED lighting upgrade",
            "description": "Replace incandescent bulbs with LED to cut lighting energy by up to 80%.",
            "priority": "low",
            "potential_savings_inr": 80,
            "category": "lighting",
        })
        if score > 2.0 or reading["estimated_bill"] > get_settings().bill_alert_threshold:
            recs.insert(0, {
                "id": "r0",
                "title": "Peak load alert",
                "description": "Current usage is in peak band. Defer heavy appliances for 2 hours.",
                "priority": "high",
                "potential_savings_inr": 350,
                "category": "peak",
            })
        return recs[:6]

    def nilm_breakdown(self, user_id: str) -> dict:
        reading = get_simulator(user_id).next_reading()
        total = reading["power_kw"]
        apps = reading["appliances"]
        return {
            "total_kw": total,
            "appliances": [
                {"name": k, "power_kw": v, "percentage": round(100 * v / total, 1) if total else 0}
                for k, v in sorted(apps.items(), key=lambda x: -x[1])
            ],
            "method": "NILM-heuristic",
        }

    def chatbot_reply(self, message: str, user_id: str) -> dict:
        msg = message.lower()
        reading = get_simulator(user_id).next_reading()
        if "bill" in msg or "cost" in msg:
            reply = (
                f"Your estimated monthly bill is ₹{reading['estimated_bill']:.0f} "
                f"based on {reading['monthly_kwh']:.1f} kWh at ₹{get_settings().tariff_per_kwh}/kWh."
            )
        elif "save" in msg or "tip" in msg:
            reply = "Try running heavy appliances after 10 PM, set AC to 26°C, and unplug standby devices."
        elif "predict" in msg or "future" in msg:
            preds = self.predict_usage(user_id, "24h")[:3]
            reply = "Next hours forecast: " + ", ".join(
                f"{p['hour']} → {p['predicted_kwh']} kWh" for p in preds
            )
        elif "carbon" in msg:
            reply = f"Your estimated carbon footprint this month is {reading['carbon_kg']:.1f} kg CO₂."
        else:
            reply = (
                "I'm your Smart Energy assistant. Ask about bills, savings tips, "
                "predictions, or carbon footprint."
            )
        return {
            "reply": reply,
            "suggestions": [
                "What is my estimated bill?",
                "How can I save energy?",
                "Show carbon footprint",
            ],
        }


ml_service = MLService()

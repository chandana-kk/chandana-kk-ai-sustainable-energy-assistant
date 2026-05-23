"""Energy and analytics schemas."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LiveEnergyReading(BaseModel):
    timestamp: datetime
    voltage: float
    current: float
    power_kw: float
    power_w: float
    frequency: float = 50.0
    power_factor: float = 0.92
    daily_kwh: float
    monthly_kwh: float
    estimated_bill: float
    carbon_kg: float
    appliances: Dict[str, float] = Field(default_factory=dict)


class EnergyHistoryPoint(BaseModel):
    label: str
    kwh: float
    cost: float


class PredictionPoint(BaseModel):
    hour: str
    predicted_kwh: float
    confidence: float = 0.85


class RecommendationItem(BaseModel):
    id: str
    title: str
    description: str
    priority: str
    potential_savings_inr: float
    category: str


class AlertItem(BaseModel):
    id: str
    type: str
    severity: str
    message: str
    created_at: datetime
    read: bool = False


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    suggestions: List[str] = Field(default_factory=list)


class IoTReading(BaseModel):
    """Placeholder for ESP32 + SCT-013 sensor payloads."""
    device_id: str
    voltage: float
    current: float
    power_w: float
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SettingsUpdate(BaseModel):
    preferred_language: Optional[str] = None
    theme: Optional[str] = None
    bill_alert_threshold: Optional[float] = None
    tariff_per_kwh: Optional[float] = None

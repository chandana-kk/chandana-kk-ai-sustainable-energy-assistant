from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class LiveReading(BaseModel):
    voltage: float
    current: float
    power_kw: float
    power_factor: float
    frequency: float
    timestamp: datetime


class ApplianceEstimate(BaseModel):
    name: str
    power_w: float
    share_percent: float
    category: str


class EnergySnapshot(BaseModel):
    live: LiveReading
    daily_kwh: float
    weekly_kwh: float
    monthly_kwh: float
    estimated_bill: float
    carbon_kg: float
    appliances: list[ApplianceEstimate]
    peak_hour: str
    savings_potential: float


class PredictionPoint(BaseModel):
    label: str
    actual: float | None = None
    predicted: float


class PredictionResponse(BaseModel):
    horizon: str
    unit: str = "kWh"
    points: list[PredictionPoint]
    peak_load_kw: float
    confidence: float


class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    impact: str
    category: str
    priority: int


class AlertItem(BaseModel):
    id: str
    type: str
    message: str
    severity: str
    created_at: datetime
    read: bool = False


class UserSettingsUpdate(BaseModel):
    language: str | None = None
    theme: str | None = None
    bill_threshold: float | None = None
    notifications_enabled: bool | None = None


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    suggestions: list[str] = Field(default_factory=list)


class TimeSeriesPoint(BaseModel):
    label: str
    value: float


class DashboardHistory(BaseModel):
    daily: list[TimeSeriesPoint]
    weekly: list[TimeSeriesPoint]
    monthly: list[TimeSeriesPoint]


class AdminStats(BaseModel):
    total_users: int
    active_sessions: int
    total_energy_kwh: float
    avg_daily_kwh: float
    system_status: str

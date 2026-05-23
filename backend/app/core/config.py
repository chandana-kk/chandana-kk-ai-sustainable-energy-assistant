"""Application configuration loaded from environment variables."""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Smart Energy AI"
    debug: bool = True

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "smart_energy_ai"

    jwt_secret_key: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    energy_sim_interval_seconds: float = 3.0
    tariff_per_kwh: float = 8.5
    bill_alert_threshold: float = 2500.0

    mqtt_enabled: bool = False
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_topic_energy: str = "home/energy/readings"

    ml_models_path: str = "../ml_models/saved_models"

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"
_BACKEND_ENV = Path(__file__).resolve().parents[2] / ".env"
_ENV_FILE = str(_ROOT_ENV if _ROOT_ENV.exists() else _BACKEND_ENV)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Smart Energy AI"
    app_env: str = "development"
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "smart_energy"
    jwt_secret_key: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    simulation_interval_seconds: int = 3
    electricity_rate_per_kwh: float = 8.5
    peak_rate_multiplier: float = 1.4
    bill_alert_threshold: float = 5000.0
    ml_models_path: str = str(Path(__file__).resolve().parents[3] / "ml_models" / "saved_models")
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_topic_energy: str = "home/energy/readings"
    mqtt_enabled: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

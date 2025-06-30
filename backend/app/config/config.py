from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    # database configuration
    DB_URL: str = "./bottles_refund_system.db"
    SEED_DB: bool = False

    # auth configuration
    API_TOKEN: str | None = None  # static token for testing purposes

    model_config = SettingsConfigDict(env_file=env_path)


settings = Settings()

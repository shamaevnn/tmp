from enum import Enum
from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class AppEnvTypes(Enum):
    PROD: str = "prod"
    DEV: str = "dev"
    TEST: str = "test"


class Settings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.PROD

    database_url: str | PostgresDsn
    max_connection_count: int = 50
    min_connection_count: int = 5

    redis_url: str = "redis://localhost:6379"

    @validator("app_env")
    def set_to_default(  # pylint: disable=no-self-argument
        cls, value: AppEnvTypes | None
    ) -> AppEnvTypes:
        if value is None:
            value = AppEnvTypes.PROD
        return value

    @property
    def db_options(self) -> dict[str, Any]:
        if "postgres" in self.database_url:
            options = {
                "min_size": self.min_connection_count,
                "max_size": self.max_connection_count,
            }
        elif "sqlite" in self.database_url:
            options = {}
        else:
            raise ValueError(f"Unknown db engine = {self.database_url}")
        return options

    @property
    def render_as_batch(self) -> bool:
        return "sqlite" in self.database_url

    class Config:
        env_file = ".env"


settings = Settings()

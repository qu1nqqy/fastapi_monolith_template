"""
Store and manage application-wide configuration.

- Load values from environment variables or .env files.
- Use typed config objects (e.g., via Pydantic or simple classes).
- Import config globally as `cfg`.

Recommended: group configs (e.g., database, logging, AWS) inside this module.
"""

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)
from pathlib import Path
from datetime import timedelta, timezone
from typing import Type

if __name__ == "__main__":
    import sys

    BASE_DIR = Path(__file__).parent.parent.parent
    sys.path.append(str(BASE_DIR))

BASE_DIR = Path(__file__).parent.parent.parent
ENV_PATH = BASE_DIR.joinpath(".env")
JSON_SETTINGS_PATH = BASE_DIR.joinpath("config.json")
TOML_SETTINGS_PATH = BASE_DIR.joinpath("config.toml")

PathsSourcesDict: dict[Path, Type[PydanticBaseSettingsSource]] = {
    TOML_SETTINGS_PATH: TomlConfigSettingsSource,
    JSON_SETTINGS_PATH: JsonConfigSettingsSource,
    ENV_PATH: EnvSettingsSource,
}


class Database(BaseModel):
    postgres_username: str = "postgres"
    postgres_db: str = "postgres"
    postgres_port: int = 5432
    postgres_host: str = "localhost"
    postgres_password: str = "postgres"

    @property
    def async_database_url(self) -> str:
        return "postgresql+asyncpg://%s:%s@%s:%d/%s" % (
            self.postgres_username,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_db,
        )


class App(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    reload: bool = False
    tz_offset_hours: float = 3
    query_param_separator: str = ";"
    default_offset: int = 0
    default_limit: int = 20
    maximum_limit: int = 151
    debug: bool = False


class Logging(BaseModel):
    level: str = "INFO"


class S3(BaseModel):
    aws_host: str = "localhost:9000"
    aws_access_key: str = ""
    aws_secret_access_key: str = ""
    aws_region: str | None = None
    aws_bucket: str = ""


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=ENV_PATH,
        json_file=JSON_SETTINGS_PATH,
        toml_file=TOML_SETTINGS_PATH,
    )

    app: App = App()
    database: Database = Database()
    logging: Logging = Logging()
    s3: S3 = S3()

    @property
    def tz(self) -> timezone:
        return timezone(
            offset=timedelta(hours=self.app.tz_offset_hours),
            name="Europe/Moscow",
        )

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        res = [
            method(settings_cls)
            for path, method in PathsSourcesDict.items()
            if path.exists()
        ]
        return EnvSettingsSource(settings_cls), *res


settings = Config()

if __name__ == "__main__":
    print(BASE_DIR)
    print(settings.model_dump_json(indent=2))

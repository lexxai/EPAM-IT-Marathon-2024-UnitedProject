import os
from pydantic import BaseModel, MySQLDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    # WEBSITE_HOSTNAME: str = "stitmarathonlexxaiprod.z16.web.core.windows.net"


class DatabaseConfig(BaseModel):
    url: MySQLDsn = ""  # type: ignore
    # Below is the temporary fix to have a proper host name for migrations!
    alembic_url: str = ""
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str = ""
    verification_token_secret: str = ""


class ApiSettings(BaseModel):
    prefix: str = "/api"
    v1_prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1_prefix, self.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            (os.path.join(os.path.dirname(__file__), "..", "..", ".env"),)
            if not os.getenv("DOCKER")
            else ()
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow",
    )
    run: RunConfig = RunConfig()
    api: ApiSettings = ApiSettings()
    db: DatabaseConfig = DatabaseConfig()
    access_token: AccessToken = AccessToken()


settings = Settings()
# print(settings)

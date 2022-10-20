import logging
import secrets
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, MongoDsn, validator


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Shortify"
    PROJECT_VERSION: str = "0.1.4"
    API_V1_STR: str = "v1"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = []

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/shortify.log"

    @validator("LOG_LEVEL")
    def log_level_validator(cls, v: str) -> str:  # noqa
        v = v.upper()
        if not hasattr(logging, v):
            raise ValueError(f"Invalid log level: {v!r}")
        return v

    @validator("LOG_FILE_PATH")
    def check_log_file_path(cls, v: str) -> str:  # noqa
        if not v.endswith(".log"):
            raise ValueError(f"Invalid log file path: {v!r} (must end with .log)")
        Path(v).parent.mkdir(parents=True, exist_ok=True)
        return v

    # Custom validators that have 'pre' set to 'True', will be called before
    # all standard pydantic validators.
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,  # noqa
        v: Union[str, List[str]],
    ) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    MONGODB_URI: MongoDsn

    # Superuser
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 60 minutes * 24 hours * 1 = 1 day
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # URLs
    URL_IDENT_LENGTH: int = 7

    class Config:
        # Place your .env file under this path
        env_file = "shortify/.env"
        env_prefix = "SHORTIFY_"
        case_sensitive = True


settings = Settings()

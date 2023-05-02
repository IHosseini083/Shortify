import secrets
from typing import List

from pydantic import BaseSettings, EmailStr, MongoDsn

from shortify import __version__
from shortify.app.core.enums import LogLevel

# This adds support for 'mongodb+srv' connection schemas when using e.g. MongoDB Atlas
MongoDsn.allowed_schemes.add("mongodb+srv")


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Shortify"
    PROJECT_VERSION: str = __version__
    API_V1_STR: str = "v1"
    DEBUG: bool = True
    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    CORS_ORIGINS: List[str] = []
    USE_CORRELATION_ID: bool = True

    UVICORN_HOST: str
    UVICORN_PORT: int

    # Logging
    LOG_LEVEL: str = LogLevel.INFO

    # MongoDB
    MONGODB_URI: MongoDsn = "mongodb://db:27017/"  # type: ignore[assignment]
    MONGODB_DB_NAME: str = "shortify"

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
        env_file = ".env"
        env_prefix = "SHORTIFY_"
        case_sensitive = True


# Missing named arguments are filled with environment variables
settings = Settings()  # type: ignore[call-arg]

import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Shortify"
    PROJECT_VERSION: str = "0.0.5"
    API_V1_STR: str = "v1"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = []

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
    MONGODB_URI: str

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
        case_sensitive = True


settings = Settings()

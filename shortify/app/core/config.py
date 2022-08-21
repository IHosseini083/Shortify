from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Shortify"
    PROJECT_VERSION: str = "0.0.1"
    API_V1_STR: str = "v1"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

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

    MONGODB_URI: str

    class Config:
        # Place your .env file under this path
        env_file = "shortify/.env"
        case_sensitive = True


settings = Settings()

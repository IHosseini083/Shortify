from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)


class LogLevel(BaseEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

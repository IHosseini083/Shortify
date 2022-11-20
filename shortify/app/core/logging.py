import logging
import logging.config
from typing import Any, Dict, Tuple

import structlog
import uvicorn

from shortify.app.core.config import settings
from shortify.app.middlewares.correlation import correlation_id

LOG_LEVEL = "DEBUG" if settings.DEBUG else settings.LOG_LEVEL

EventDict = structlog.typing.EventDict


def add_correlation_id(_, __, event_dict: EventDict) -> EventDict:
    if cid := correlation_id.get():
        event_dict["correlation_id"] = cid
    return event_dict


def remove_color_message(_, __, event_dict: EventDict) -> EventDict:
    event_dict.pop("color_message", None)
    return event_dict


# Processors that have nothing to do with output,
# e.g. add timestamps or log level names.
SHARED_PROCESSORS: Tuple[structlog.types.Processor, ...] = (
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_log_level,
    # Add extra attributes of LogRecord objects to the event dictionary
    # so that values passed in the extra parameter of log methods pass
    # through to log output.
    structlog.stdlib.ExtraAdder(),
    # Add a timestamp in ISO 8601 format.
    structlog.processors.TimeStamper(fmt="ISO"),
)
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            # Render the final event dict as JSON.
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": SHARED_PROCESSORS + (add_correlation_id,),
        },
        "colored": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processors": [
                remove_color_message,
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            "foreign_pre_chain": SHARED_PROCESSORS,
        },
        **uvicorn.config.LOGGING_CONFIG["formatters"],
    },
    "handlers": {
        "default": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.FileHandler",
            "filename": settings.LOG_FILE_PATH,
            "formatter": "json",
        },
        "uvicorn.access": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "access",
        },
        "uvicorn.default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "uvicorn.error": {
            "handlers": ["default" if not settings.DEBUG else "uvicorn.default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default" if not settings.DEBUG else "uvicorn.access"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    # noinspection PyTypeChecker
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            *SHARED_PROCESSORS,
            structlog.stdlib.PositionalArgumentsFormatter(),
            # If the "stack_info" key in the event dict is true, remove it and
            # render the current stack trace in the "stack" key.
            structlog.processors.StackInfoRenderer(),
            # If the "exc_info" key in the event dict is either true or a
            # sys.exc_info() tuple, remove "exc_info" and render the exception
            # with traceback into the "exception" key.
            structlog.processors.format_exc_info,
            # If some value is in bytes, decode it to a unicode str.
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

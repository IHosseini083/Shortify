import logging
import logging.config
from typing import Any, Dict, Tuple

import structlog
import uvicorn

from shortify.app.core.config import settings

# Processors that have nothing to do with output,
# e.g. add timestamps or log level names.
SHARED_PROCESSORS: Tuple[structlog.types.Processor, ...] = (
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    # Add a timestamp in ISO 8601 format.
    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
    # Add extra attributes of LogRecord objects to the event dictionary
    # so that values passed in the extra parameter of log methods pass
    # through to log output.
    structlog.stdlib.ExtraAdder(),
)

LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            # Render the final event dict as JSON.
            "processor": structlog.processors.JSONRenderer(indent=4, sort_keys=True),
            "foreign_pre_chain": SHARED_PROCESSORS,
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": SHARED_PROCESSORS,
        },
        **uvicorn.config.LOGGING_CONFIG["formatters"],
    },
    "handlers": {
        "default": {
            "level": settings.LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "json" if not settings.DEBUG else "console",
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
            "handlers": ["default"],
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
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.config.dictConfig(LOGGING_CONFIG)

"""
Correlation ID middleware implementation inspired from asgi-correlation-id project:
https://github.com/snok/asgi-correlation-id
"""
import sys
from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable, Optional
from uuid import UUID, uuid4

import structlog
from starlette.datastructures import Headers, MutableHeaders

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Message, Receive, Scope, Send
    from structlog.stdlib import BoundLogger

logger: "BoundLogger" = structlog.get_logger()

# Context variable to store the correlation ID
correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)

IDGenerator: TypeAlias = Callable[[], str]
IDValidator: TypeAlias = Callable[[str], bool]
IDTransformer: TypeAlias = Callable[[str], str]


def is_valid_uuid4(uuid_string: str) -> bool:
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True


class CorrelationMiddleware:
    __slots__ = (
        "app",
        "header",
        "id_generator",
        "id_validator",
        "id_transformer",
    )

    def __init__(
        self,
        app: "ASGIApp",
        *,
        header: str = "X-Request-ID",
        id_generator: IDGenerator = lambda: uuid4().hex,
        id_validator: Optional[IDValidator] = is_valid_uuid4,
        id_transformer: Optional[IDTransformer] = lambda x: x,
    ) -> None:
        self.app = app
        self.header = header
        self.id_generator = id_generator
        self.id_validator = id_validator
        self.id_transformer = id_transformer

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        header_value = Headers(scope=scope).get(self.header)
        if not header_value:
            id_ = self.id_generator()
        elif self.id_validator and not self.id_validator(header_value):
            id_ = self.id_generator()
            await logger.awarning(
                "Generated new correlation ID because the provided one was invalid",
                correlation_id=id_,
            )
        else:
            id_ = header_value

        if self.id_transformer:
            id_ = self.id_transformer(id_)

        correlation_id.set(id_)

        async def send_wrapper(message: "Message") -> None:
            if message["type"] == "http.response.start" and (
                cid := correlation_id.get()
            ):
                headers = MutableHeaders(scope=message)
                headers[self.header] = cid
                headers["Access-Control-Expose-Headers"] = self.header
            await send(message)

        await self.app(scope, receive, send_wrapper)

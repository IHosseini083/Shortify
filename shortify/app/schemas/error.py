from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from pydantic import ValidationError


class ValidationErrorDetail(BaseModel):
    location: str
    message: str
    error_type: str
    context: Optional[Dict[str, Any]] = None


class APIValidationError(BaseModel):
    errors: List[ValidationErrorDetail]

    @classmethod
    def from_pydantic(cls, exc: "ValidationError") -> "APIValidationError":
        return cls(
            errors=[
                ValidationErrorDetail(
                    location=" -> ".join(map(str, err["loc"])),
                    message=err["msg"],
                    error_type=err["type"],
                    context=err.get("ctx"),
                )
                for err in exc.errors()
            ],
        )

    class Config:
        schema_extra = {
            "example": {
                "errors": [
                    {
                        "origin": "body -> url",
                        "message": "invalid or missing URL scheme",
                        "error_type": "value_error.url.scheme",
                    },
                ],
            },
        }


class CommonHTTPError(BaseModel):
    """JSON response model for errors raised by :class:`starlette.HTTPException`."""

    message: str
    extra: Optional[Dict[str, Any]] = None

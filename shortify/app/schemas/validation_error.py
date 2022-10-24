from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ValidationError


class Error(BaseModel):
    location: str
    message: str
    error_type: str
    context: Optional[Dict[str, Any]] = None


class APIValidationError(BaseModel):
    """Schema for validation errors returned by the API with HTTP status code 422"""

    errors: List[Error]

    @classmethod
    def from_pydantic(cls, exc: ValidationError) -> "APIValidationError":
        """Create a new APIValidationError from a pydantic ValidationError"""
        return cls(
            errors=[
                Error(
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

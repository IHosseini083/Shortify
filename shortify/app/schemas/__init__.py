from typing import Generic, List, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

from .token import AuthToken, AuthTokenPayload
from .url import ShortUrl, ShortUrlCreate
from .user import User, UserCreate, UserInDB, UserUpdate

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Paginated(GenericModel, Generic[SchemaType]):
    page: int
    per_page: int
    total: int
    results: List[SchemaType]

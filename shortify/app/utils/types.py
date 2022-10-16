from typing import Any, List, TypedDict


class PaginationDict(TypedDict):
    page: int
    per_page: int
    total: int
    results: List[Any]

from typing import TYPE_CHECKING, Type, TypeVar

from beanie import Document

from shortify.app.utils.types import PaginationDict

if TYPE_CHECKING:
    from shortify.app.schemas import PaginationParams, SortingParams

DocumentType = TypeVar("DocumentType", bound=Document)


async def paginate(
    document: Type[DocumentType],
    paging_params: "PaginationParams",
    sorting_params: "SortingParams",
) -> PaginationDict:
    results = (
        await document.find()
        .skip(paging_params.skip)
        .limit(paging_params.limit)
        .sort(
            (sorting_params.sort, sorting_params.order.direction),
        )
        .to_list()
    )
    return {
        "page": paging_params.page,
        "per_page": paging_params.per_page,
        "total": await document.count(),
        "results": results,
    }

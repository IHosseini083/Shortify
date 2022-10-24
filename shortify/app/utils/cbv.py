"""Class-based views, borrowed from fastapi-utils project with a few modifications."""
import inspect
from typing import Any, Callable, List, Type, TypeVar, Union, get_type_hints

from fastapi import APIRouter, Depends
from pydantic.typing import is_classvar
from starlette.routing import Route, WebSocketRoute

_T = TypeVar("_T")

_CBV_KEY = "__cbv_initialized__"


def _init_cbv(cls: Type[Any]) -> None:
    """
    Idempotently modifies the provided `cls`, performing the following modifications:
    * The `__init__` method is updated to set any class-annotated dependencies
    as instance attributes.
    * The `__signature__` attribute is updated to indicate to FastAPI what arguments
    should be passed to the initializer.
    """
    if getattr(cls, _CBV_KEY, False):
        return  # Already initialized
    init_method: Callable[..., None] = cls.__init__  # noqa
    signature = inspect.signature(init_method)
    parameters = list(signature.parameters.values())[1:]  # Drop `self` parameter
    new_parameters = [
        p
        for p in parameters
        if p.kind
        not in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        )
    ]
    dependency_names: List[str] = []
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(
                name=name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                annotation=hint,
                **parameter_kwargs,
            ),
        )
    new_signature = signature.replace(parameters=new_parameters)

    def new_init_method(self: Any, *args: Any, **kwargs: Any) -> None:
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        init_method(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init_method)
    setattr(cls, _CBV_KEY, True)


def _update_cbv_route_endpoint_signature(
    cls: Type[Any],
    route: Union[Route, WebSocketRoute],
) -> None:
    """
    Fixes the endpoint signature for a class-based view route to ensure that
    FastAPI performs dependency injection properly.
    """
    signature = inspect.signature(route.endpoint)
    parameters: List[inspect.Parameter] = list(signature.parameters.values())
    new_parameters = [parameters[0].replace(default=Depends(cls))] + [
        p.replace(kind=inspect.Parameter.KEYWORD_ONLY) for p in parameters[1:]
    ]
    new_signature = signature.replace(parameters=new_parameters)
    setattr(route.endpoint, "__signature__", new_signature)


def cbv(router: APIRouter) -> Callable[[Type[_T]], Type[_T]]:
    """
    Returns a decorator that converts the decorated into a class-based view
    for the provided router.

    Any methods of the decorated class that are decorated as endpoints using
    the router provided to this function will become endpoints in the router.
    The first positional argument to the methods (typically `self`)
    will be populated with an instance created using FastAPI's dependency-injection.
    """

    def dec(cls: Type[_T]) -> Type[_T]:
        _init_cbv(cls)
        view_router = APIRouter()
        functions = {func for _, func in inspect.getmembers(cls, inspect.isfunction)}
        view_routes = [
            route
            for route in router.routes
            if isinstance(route, (Route, WebSocketRoute))
            and route.endpoint in functions
        ]
        for route in view_routes:
            router.routes.remove(route)
            _update_cbv_route_endpoint_signature(cls, route)
            view_router.routes.append(route)
        router.include_router(view_router)
        return cls

    return dec

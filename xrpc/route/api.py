from typing import Callable, Dict, Tuple
from xrpc.route.request import Request
import functools

_routes = dict()

Response = Tuple | int | str | dict


def handler(method: str, path: str) -> Callable:
    def handler_decorator(fn: Callable):
        add_route(method, path, fn)

        @functools.wraps
        def handler_internal(*args, **kwargs):
            fn(*args, **kwargs)
        return handler_internal
    return handler_decorator


def add_route(method: str, path: str, fn: Callable):
    if path not in _routes:
        _routes[path] = dict()
    _routes[path][method] = fn


def get_route(method: str, path: str) -> Callable:
    return _routes.get(path, dict()).get(method, None)


def get_routes(path: str) -> Dict:
    return _routes.get(path, dict())


def route(request: Request) -> Response:
    fn = get_route(request.method, request.path)
    return fn(request) if fn else (404, {'msg': 'No such path'})

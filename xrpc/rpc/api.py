
from typing import Callable, Dict
from xrpc.rpc.rpc import RPC
from xrpc.rpc.response import Response
from xrpc.rpc.request import Request
from xrpc.log import logger
import functools
import requests


_rpcs = dict()


def call(name: str, params: Dict = dict(), host: str = 'localhost', port: int = 8080) -> Response:
    res = requests.post(f'http://{host}:{port}/rpc/call?name={name}', json=params)
    return Response(res.status_code, res.json())


def register(name: str, handler: Callable):
    _rpcs[name] = RPC(name, handler)


def handler(fn: Callable):
    _rpcs[fn.__name__] = RPC(fn.__name__, fn)
    @functools.wraps(fn)
    def handler_wrapper(*args, **kwargs):
        fn(*args, **kwargs)
    return handler_wrapper


class remote:
    @staticmethod
    def register(name: str, handler: Callable, host: str = 'localhost', port: int = 8080):
        _rpcs[name] = RPC(name, handler, (host, port))
        _rpcs[name].register()
        pass

    def handler(host: str = 'localhost', port: int = 8080):
        def handler_internal(fn: Callable):
            _rpcs[fn.__name__] = RPC(fn.__name__, handler, (host, port))
            _rpcs[fn.__name__].register()
            @functools.wraps(fn)
            def handler_wrapper(*args, **kwargs):
                fn(*args, **kwargs)
            return handler_wrapper
    
    def unregister_all():
        for rpc in _rpcs.values():
            logger.debug(f'Unregister {rpc.name}') # ?
            rpc.unregister()



def get_rpc(name: str) -> Callable:
    return _rpcs.get(name, None)


def get_rpcs() -> Dict:
    return _rpcs
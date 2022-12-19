from .rpc_server import RPCServer

_server = None


def run(port: int = 8080):
    global _server
    _server = RPCServer(port)
    _server.run_async()


def join():
    if _server:
        _server.join()


def get_port() -> int:
    return _server.port if _server else 0


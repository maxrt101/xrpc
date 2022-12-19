from typing import Dict, Tuple
from xrpc.rpc.api import Request, Response
from xrpc.rpc.api import call as rpc_call
from xrpc.rpc.api import get_rpc
from xrpc.log import logger
from xrpc.util import addr_to_str


_remote_rpcs = dict()


def _call_rpc(name: str, sender: Tuple, data: Dict) -> Response:
    rpc = get_rpc(name)
    if rpc:
        logger.debug(f'Call RPC {name} from {addr_to_str(sender)}')
        return rpc.handler(Request(name, sender, data))
    elif name in _remote_rpcs: # Proxy call
        logger.debug(f'Call remote RPC {name} from {addr_to_str(sender)}')
        return rpc_call(name, data, _remote_rpcs[name][0], _remote_rpcs[name][1])
    else:
        logger.error(f'Attempt to call non existing RPC {name} from {addr_to_str(sender)}')
        return Response(404, {'msg': f'RPC {name} not found'})


def _get_remote_rpcs() -> Dict:
    return _remote_rpcs

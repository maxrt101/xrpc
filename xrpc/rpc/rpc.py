
from typing import Callable, Tuple
from ..util import addr_to_str
from ..log import logger
import requests

class RPC:
    def __init__(self, name: str, handler: Callable, remote: Tuple = ('', 0)):
        self.name = name
        self.handler = handler
        self.remote = remote
    
    def register(self):
        from ..server.api import get_port
        if len(self.remote[0]) and self.remote[1]:
            res = requests.post(f'http://{addr_to_str(self.remote)}/rpc/register?name={self.name}&port={get_port()}')
            if res.status_code != 200:
                logger.error(f'Failed to register RPC {self.name} to {addr_to_str(self.remote)}')
        else:
            logger.error(f'Attempt to register RPC {self.name} to invalid remote')
    
    def unregister(self):
        if len(self.remote[0]) and self.remote[1]:
            res = requests.post(f'http://{addr_to_str(self.remote)}/rpc/unregister?name={self.name}')
            if res.status_code != 200:
                logger.error(f'Failed to unregister RPC {self.name} from {addr_to_str(self.remote)}')

from typing import Dict, Tuple
from xrpc.util import addr_to_str


class Request:
    def __init__(self, rpc_name: str = '', sender: Tuple = ('', 0), params: Dict = dict()):
        self.rpc_name = rpc_name
        self.sender = sender
        self.params = params
    
    def __repr__(self) -> str:
        return f'<Request [{self.rpc_name}] from {addr_to_str(self.sender)}>'

    def __str__(self) -> str:
        return f'Request(name={self.rpc_name}, sender={self.sender}, params={self.params})'

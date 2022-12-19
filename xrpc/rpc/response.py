
from typing import Dict


class Response:
    def __init__(self, code: int = 200, data: Dict = dict()):
        self.code = code
        self.data = data

    def __repr__(self) -> str:
        return f'<Response [{self.code}]>'
    
    def __str__(self) -> str:
        return f'Response(code={self.code}, data={self.data})'

    @classmethod
    def ok(cls, data: Dict = dict()) -> 'Response':
        return cls(200, data)

    @classmethod
    def fail(cls, data: Dict = dict()) -> 'Response':
        return cls(400, data)

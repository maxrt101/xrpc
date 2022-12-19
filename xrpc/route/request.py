from typing import Dict


class Request:
    def __init__(self, method: str, path: str, params: Dict, headers: Dict, body: str):
        self.method = method
        self.path = path
        self.params = params
        self.headers = headers
        self.body = body

    def __repr__(self) -> str:
        return f'<Request {self.method} {self.path}>'

    def __str__(self) -> str:
        return f'Request(method={self.method} path={self.path}, params={self.params}, headers={self.headers}, body={self.body})'


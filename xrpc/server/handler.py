from http.server import BaseHTTPRequestHandler
from typing import Dict, Tuple
from urllib.parse import urlparse
from xrpc.route.api import get_route, Response as RouteResponse, Request as RouteRequest
from xrpc.rpc.api import get_rpcs
from xrpc.log import logger
from xrpc.server.rpc import _call_rpc, _get_remote_rpcs
import builtins
import json


class ServerHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, code: int, data: str | dict = '', headers: Dict = dict()):
        self.send_response(code)
        for header, value in headers.items():
            self.send_header(header, value)
        if type(data) == dict and 'Content-Type' not in headers:
            self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write((json.dumps(data) if type(data) == dict else str(data)).encode())

    def _send_response_from_tuple(self, response: Tuple):
        match len(response):
            case 0:
                self._send_response(200)
            case 1:
                self._send_response(response[0])
            case 2:
                self._send_response(response[0], json.dumps(response[1]) if type(response[1]) == dict else str(response[1]))
            case x if x >= 3:
                self._send_response(response[0], json.dumps(response[1]) if type(response[1]) == dict else str(response[1]), response[2])
            case _:
                self._send_response(500, {'msg': 'Invalid route response'})

    def _send_response_from_route(self, response: RouteResponse):
        match type(response):
            case builtins.tuple:
                self._send_response_from_tuple(response)
            case builtins.int:
                self._send_response(response)
            case builtins.str:
                self._send_response(200, response)
            case builtins.dict:
                self._send_response(200, response)

    def do_GET(self):
        logger.info("GET %s", str(self.path))
        try:
            url = urlparse(self.path)
            params = {k: v for k, v in [kv.split('=') for kv in url.query.split('&')]} if url.query else {}
            if url.path == '/rpc/list':
                self._send_response(200, {'rpcs': list(get_rpcs().keys()), 'remote_rpcs': list(_get_remote_rpcs().keys())})
            else:
                if route := get_route('GET', url.path):
                    self._send_response_from_route(route(RouteRequest('GET', url.path, params, self.headers, '')))
                else:
                    self._send_response(404, {'msg': 'Invalid path'})
        except Exception as e:
            logger.error(str(e))
            self._send_response(500, {'msg': 'Internal Error'})

    def do_POST(self):
        logger.info("POST %s", str(self.path))
        try:
            url = urlparse(self.path)
            params = {k: v for k, v in [kv.split('=') for kv in url.query.split('&')]} if url.query else {}
            if url.path == '/rpc/call':
                if 'name' not in params:
                    self._send_response(401, {'msg': 'Expected RPC name'})
                    return
                content_len = int(self.headers.get('Content-Length'))
                rpc_response = _call_rpc(
                    params['name'],
                    self.client_address,
                    json.loads(self.rfile.read(content_len)) if content_len else {}
                )
                self._send_response(rpc_response.code, rpc_response.data)
            elif url.path == '/rpc/register':
                if 'name' not in params or 'port' not in params:
                    self._send_response(401, {'msg': 'Expected RPC name and port'})
                    return
                _get_remote_rpcs()[params['name']] = (self.client_address[0], params['port'])
                self._send_response(200, {'msg': 'ok'})
            else:
                if route := get_route('GET', url.path):
                    content_len = int(self.headers.get('Content-Length'))
                    body = self.rfile.read(content_len) if content_len else ''
                    self._send_response_from_route(route(RouteRequest('POST', url.path, params, self.headers, body)))
                else:
                    self._send_response(404, {'msg': 'Invalid path'})
        except Exception as e:
            logger.error(str(e))
            self._send_response(500, {'msg': 'Internal Error'})

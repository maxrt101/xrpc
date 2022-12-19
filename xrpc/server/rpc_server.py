from http.server import HTTPServer
from xrpc.rpc.api import remote
from xrpc.log import logger
from xrpc.server.handler import ServerHTTPRequestHandler
import threading


class RPCServer:
    def __init__(self, port: int, handler = ServerHTTPRequestHandler, server = HTTPServer):
        self.port = port
        self.handler_class = handler
        self.server_class = server
        self.server = self.server_class(('', self.port), self.handler_class)
        self.thread = None

    def _serve(self):
        try:
            self.server.serve_forever()
        except (Exception, KeyboardInterrupt) as e:
            remote.unregister_all()

    def run(self):
        logger.info(f'Staring RPC server (sync) on {self.port}')
        self._serve()

    def run_async(self):
        logger.info(f'Staring RPC server (async) on {self.port}')
        self.thread = threading.Thread(target=self._serve)
        self.thread.start()
    
    def join(self):
        self.thread.join()


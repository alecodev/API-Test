#!/usr/bin/env python3
import os
import sys
import json
import signal
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import re
import importlib
from tests import tests


class router(BaseHTTPRequestHandler):

    _http_code = 200
    _endpoints = {
        '/realEstates': {
            '/': 'realEstates',
            '/(\d+)/Likes': 'realEstates_Likes'
        }
    }

    def _request(self):
        # Load data from request
        _method = self.command
        _header_accept = self.headers.get_param('Accept', 'application/json')
        _endpoint = re.sub(r"(^\/|\/$)", "", re.sub(r"\/\/+",
                           "/", self.path), 0).split('/')

        _resource = '/' + _endpoint.pop(0)
        _sub_resource = '/' + '/'.join(_endpoint)
        _pattern = self._exist_endpoint(_resource, _sub_resource)
        if _pattern == False:
            self._http_code = 404
        else:
            _header_content_type = self.headers.get_param(
                'Content-Type', 'application/json')

            matches = re.search(r"^"+_pattern+"$", _sub_resource)
            _args = matches.groups() if matches and matches.groups() else ()
            _data = None

            module = importlib.import_module(
                'resources.'+self._endpoints[_resource][_pattern])
            if (not hasattr(module, 'endpoint')) or (not hasattr(module.endpoint, 'do_'+_method)):
                self._http_code = 404
            else:
                result = getattr(module.endpoint(), 'do_' +
                                 _method)(args=_args, data=_data)

        # Set response
        self.send_response(self._http_code)
        self.send_header('Content-Type', _header_accept)
        self.end_headers()

    def _exist_endpoint(self, _resource='', _sub_resource=''):
        if _resource in self._endpoints:
            for _pattern in self._endpoints[_resource]:
                if re.fullmatch(r"^"+_pattern+"$", _sub_resource) != None:
                    return _pattern
        return False

    def do_GET(self):
        self._request()

    def do_POST(self):
        self._request()

    def do_PUT(self):
        self._request()

    def do_PATCH(self):
        self._request()

    def do_DELETE(self):
        self._request()

    def log_message(self, format, *args):
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class App(object):

    server = None
    server_thread = None

    def run(self, host: str = '0.0.0.0',  port: int = 5000):
        self.server = ThreadedHTTPServer((host, port), router)
        print('🚀 API Running %s on port %s' % (HOST, str(PORT)))
        try:
            self.server_thread = threading.Thread(
                target=self.server.serve_forever, daemon=True)
            self.server_thread.start()

        except Exception as e:
            print(e)

    def waitForThread(self):
        self.server_thread.join()

    def __del__(self):
        if self.server:
            self.server.shutdown()


if __name__ == '__main__':

    # Función para notificar el cierre del proceso
    def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

    # Ctrl + C
    signal.signal(signal.SIGINT, def_handler)

    # Configuración de variables de entorno
    INTERNAL_HOST = str(os.environ['APP_INTERNAL_HOST'])
    HOST = str(os.environ['APP_HOST'])
    PORT = int(os.environ['APP_PORT'])
    URL = 'http://%s:%s' % (HOST, str(PORT))

    # Inicialización del servidor
    app = App()
    app.run(INTERNAL_HOST, PORT)

    # Validación de sí existen argumentos en la línea de comandos
    if (len(sys.argv) - 1) > 0:
        arguments = sys.argv[1:]
        if '-t' in arguments or '--test' in arguments:
            tests().run(url=URL)
            sys.exit(0)

    app.waitForThread()

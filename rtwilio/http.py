import select
import SocketServer

from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler


class TwilioHandler(WSGIHandler):
    """ WSGIHandler without Django middleware calls """

    def __call__(self, environ, start_response):
        request = self.request_class(environ)
        response = self.backend.handle_request(request)
        status = '%s %s' % (response.status_code, 'OK')
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        start_response(status, response_headers)
        return response


class HttpServer(WSGIServer, SocketServer.ThreadingMixIn):
    """ WSGIServer that doesn't block on handle_request """

    def handle_request(self, timeout=1.0):
        reads, writes, errors = (self, ), (), ()
        reads, writes, errors = select.select(reads, writes, errors, timeout)
        if reads:
            WSGIServer.handle_request(self)

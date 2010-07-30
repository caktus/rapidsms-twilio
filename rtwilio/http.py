import select
import SocketServer

from django import http
from django.core.handlers.wsgi import WSGIHandler, STATUS_CODE_TEXT
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler

from rapidsms.log.mixin import LoggerMixin


class TwilioHandler(WSGIHandler, LoggerMixin):
    """ WSGIHandler without Django middleware and signal calls """

    def _logger_name(self):
        return 'backend/twilio/handler'

    def __call__(self, environ, start_response):
        request = self.request_class(environ)
        try:
            response = self.backend.handle_request(request)
        except Exception, e:
            self.exception(e)
            response = http.HttpResponseServerError()
        try:
            status_text = STATUS_CODE_TEXT[response.status_code]
        except KeyError:
            status_text = 'UNKNOWN STATUS CODE'
        status = '%s %s' % (response.status_code, status_text)
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

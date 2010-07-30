import urllib
import urlparse
import pprint
import datetime
import SocketServer
import BaseHTTPServer
import select

from django.http import HttpResponse
from django.db import DatabaseError
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler
from django.core.handlers.wsgi import WSGIHandler

from rapidsms.backends.base import BackendBase
from rapidsms.log.mixin import LoggerMixin


class TwilioHandler(WSGIHandler, LoggerMixin):

    def __call__(self, environ, start_response):
        request = self.request_class(environ)
        response = self.backend.handle_request(request)
        status = '%s %s' % (response.status_code, 'OK')
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        start_response(status, response_headers)
        return response


class TwilioBackend(BackendBase):
    '''A RapidSMS backend for Twilio (http://www.twilio.com/)'''

    def configure(self, host="localhost", port=8080, **kwargs):
        self.host = host
        self.port = port
        self.handler = TwilioHandler()
        self.handler.backend = self

    def run(self):    
        server_address = (self.host, int(self.port))
        self.debug('Starting HTTP server on {0}:{1}'.format(*server_address))
        self.server = WSGIServer(server_address, WSGIRequestHandler)
        self.server.set_app(self.handler)
        while self.running:
            self.server.handle_request()

    def handle_request(self, request):
        message = self.message(request.GET)
        self.route(message)
        return HttpResponse('OK')

    def send(self, message):
        self.debug('send: %s' % message)

    def message(self, data):
        self.debug('message')
        now = datetime.datetime.utcnow()
        sms = data['Body']
        sender = data['From']
        self.debug('{0} {1} {2}'.format(sender, sms, now))
        try:
            msg = super(TwilioBackend, self).message(sender, sms, now)
        except DatabaseError, e:
            self.exception(e)
            raise
        self.debug(msg)
        return msg

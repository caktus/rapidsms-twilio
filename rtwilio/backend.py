import pprint
import datetime

from django.db import DatabaseError
from django.http import HttpResponse
from django.core.servers.basehttp import WSGIRequestHandler

from rapidsms.backends.base import BackendBase

from rtwilio.http import RapidHttpServer, RapidWSGIHandler


class TwilioBackend(BackendBase):
    """ A RapidSMS backend for Twilio (http://www.twilio.com/) """

    def configure(self, host="localhost", port=8080, **kwargs):
        self.host = host
        self.port = port
        self.handler = RapidWSGIHandler()
        self.handler.backend = self

    def run(self):
        server_address = (self.host, int(self.port))
        self.debug('Starting HTTP server on {0}:{1}'.format(*server_address))
        self.server = RapidHttpServer(server_address, WSGIRequestHandler)
        self.server.set_app(self.handler)
        while self.running:
            self.server.handle_request()

    def handle_request(self, request):
        message = self.message(request.GET)
        self.route(message)
        return HttpResponse('OK')

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

    def send(self, message):
        self.debug('send: %s' % message)

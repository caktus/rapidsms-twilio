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
        self.info('Starting HTTP server on {0}:{1}'.format(*server_address))
        self.server = RapidHttpServer(server_address, WSGIRequestHandler)
        self.server.set_app(self.handler)
        while self.running:
            self.server.handle_request()

    def handle_request(self, request):
        self.debug('Request: %s' % pprint.pformat(dict(request.GET)))
        message = self.message(request.GET)
        if message:
            self.route(message)
        return HttpResponse('OK')

    def message(self, data):
        sms = data.get('Body', '')
        sender = data.get('From', '')
        if not sms or sender:
            self.error('Missing Body or From: %s' % pprint.pformat(dict(data)))
            return None
        now = datetime.datetime.utcnow()
        try:
            msg = super(TwilioBackend, self).message(sender, sms, now)
        except DatabaseError, e:
            self.exception(e)
            raise
        self.debug(msg)
        return msg

    def send(self, message):
        self.debug('send: %s' % message)

import urllib
import urlparse
import pprint
import datetime

from django.http import QueryDict
from django.db import DatabaseError

from rapidsms.log.mixin import LoggerMixin
from rapidsms.backends.http import Backend, HttpServer
from rapidsms.backends.httphandlers import RapidBaseHttpHandler


class TwilioBackend(Backend):
    '''A RapidSMS backend for Twilio (http://www.twilio.com/)'''

    _title = "Twilio"

    def _logger_name(self):
        return 'twilio-backend'

    def configure(self, host="localhost", port=8080, handler="HttpHandler",
                  **kwargs):
        self.handler = TwilioHandler
        self.debug('Starting Twilio HTTP server on {0}:{1}'.format(host, port))
        self.server = HttpServer((host, int(port)), self.handler)
        self.type = "HTTP"
        # set this backend in the server instance so it
        # can callback when a message is received
        self.server.backend = self
        # also set it in the handler class so we can callback
        self.handler.backend = self
        # set the slug based on the handler, so we can have multiple
        # http backends
        self._slug = "http_%s" % handler

    def parse_POST(self, data):
        data = QueryDict(data)
        self.debug('POST data: {0}'.format(pprint.pformat(data)))
        return data

    def message(self, data):
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


class TwilioHandler(RapidBaseHttpHandler, LoggerMixin):
    '''An HTTP server that handles messages to and from Twilio '''
    # http://demo.twilio.com/welcome/sms

    def _logger_name(self):
        return 'twilio-handler'

    def do_POST(self):
        self.debug('POST')
        content_length = self.headers['Content-Length']
        data = self.rfile.read(int(content_length))
        data = self.server.backend.parse_POST(data)
        message = self.server.backend.message(data)
        self.server.backend.route(message)
        return

    @classmethod
    def outgoing(class_, message):
        class_.backend.info("outgoing: {0}".format(message))
        self.respond(200,'''
        <Response>
            <Sms>%s</Sms>
        </Response>
        ''' % message)

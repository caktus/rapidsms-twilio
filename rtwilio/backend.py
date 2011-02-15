import pprint
import datetime
import twilio

from django.db import DatabaseError
from django.http import HttpResponse
from django.core.servers.basehttp import WSGIRequestHandler

from rapidsms.backends.http import RapidHttpBacked


class TwilioBackend(RapidHttpBacked):
    """ A RapidSMS backend for Twilio (http://www.twilio.com/) """

    api_version = '2008-08-01'

    def configure(self, host="localhost", port=8080, config=None, **kwargs):
        super(TwilioBackend, self).configure(host, port, **kwargs)
        self.config = config
        self.account = twilio.Account(self.config['account_sid'],
                                      self.config['auth_token'])

    def handle_request(self, request):
        self.debug('Request: %s' % pprint.pformat(dict(request.POST)))
        message = self.message(request.POST)
        if message:
            self.route(message)
        return HttpResponse('OK')

    def message(self, data):
        sms = data.get('Body', '')
        sender = data.get('From', '')
        if not sms or not sender:
            self.error('Missing Body or From: %s' % pprint.pformat(dict(data)))
            return None
        now = datetime.datetime.utcnow()
        try:
            msg = super(TwilioBackend, self).message(sender, sms, now)
        except DatabaseError, e:
            self.exception(e)
            raise
        return msg

    def send(self, message):
        self.info('Sending message: %s' % message)
        data = {
            'From': self.config['number'],
            'To': message.connection.identity,
            'Body': message.text,
        }
        if 'callback' in self.config:
            data['StatusCallback'] = self.config['callback']
        self.debug('POST data: %s' % pprint.pformat(data))
        url = '/%s/Accounts/%s/SMS/Messages' % (self.api_version,
                                                self.config['account_sid'])
        try:
            response = self.account.request(url, 'POST', data)
        except Exception, e:
            self.exception(e.read())
            response = None
        if response:
            self.info('SENT')
            self.debug(response)

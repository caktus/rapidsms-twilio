import pprint
import datetime
import twilio

from django.db import DatabaseError
from django.http import HttpResponse
from django.core.servers.basehttp import WSGIRequestHandler

from rapidsms.backends.http import RapidHttpBackend
from urllib2 import HTTPError


compatible_api_versions = ["2008-08-01", "2010-04-01"]

class APIVersionError(Exception):
    pass

class TwilioBackend(RapidHttpBackend):
    """ A RapidSMS backend for Twilio (http://www.twilio.com/) """

    def configure(self, host="localhost", port=8080, config=None, **kwargs):
                  
        super(TwilioBackend, self).configure(host, port, **kwargs)
        self.config = config
        self.account = twilio.Account(self.config['account_sid'],
                                      self.config['auth_token'])
        
        # has the added benefit of failing hard if this is set wrong
        self.debug("using api version %s" % self.api_version)

    @property
    def api_version(self):
        version = self.config.get("api_version", "2008-08-01")
        if version not in compatible_api_versions:
            raise APIVersionError("Allowed values for api_version are %s" %\
                                  ", ".join(compatible_api_versions))
        
        
    
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
        encoding = self.config.get('encoding', 'ascii')
        if encoding and not isinstance(sms, unicode):
            sms = sms.decode(encoding)
        now = datetime.datetime.utcnow()
        try:
            msg = super(TwilioBackend, self).message(sender, sms, now)
        except DatabaseError, e:
            self.exception(e)
            raise
        return msg

    def prepare_message(self, message):
        encoding = self.config.get('encoding', 'ascii')
        encoding_errors = self.config.get('encoding_errors', 'ignore')
        data = {
            'From': self.config['number'],
            'To': message.connection.identity,
            'Body': message.text.encode(encoding, encoding_errors),
        }
        if 'callback' in self.config:
            data['StatusCallback'] = self.config['callback']
        return data

    def send(self, message):
        self.info('Sending message: %s' % message)
        data = self.prepare_message(message)
        self.debug('POST data: %s' % pprint.pformat(data))
        url = '/%s/Accounts/%s/SMS/Messages' % (self.api_version,
                                                self.config['account_sid'])
        try:
            response = self.account.request(url, 'POST', data)
        except HTTPError, e:
            self.exception(e)
            self.error("Response from twilio: %s" % e.read())
            return False
        except Exception, e:
            self.exception(e)
            return False
        self.info('SENT')
        self.debug(response)
        return True

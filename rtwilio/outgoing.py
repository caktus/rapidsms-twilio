import pprint
import datetime
from twilio.rest import TwilioRestClient

from rapidsms.backends.base import BackendBase


class TwilioBackend(BackendBase):
    """A RapidSMS backend for Twilio (http://www.twilio.com/)."""

    def start(self):
        """Override BackendBase.start(), which never returns."""
        self._running = True

    def configure(self, config=None, **kwargs):
        self.config = config
        self.client = TwilioRestClient(self.config['account_sid'],
                                       self.config['auth_token'])

    def prepare_message(self, message):
        encoding = self.config.get('encoding', 'ascii')
        encoding_errors = self.config.get('encoding_errors', 'ignore')
        data = {
            'from_': self.config['number'],
            'to': message.connection.identity,
            'body': message.text.encode(encoding, encoding_errors),
        }
        if 'callback' in self.config:
            data['status_callback'] = self.config['callback']
        return data

    def send(self, message):
        self.info('Sending message: %s' % message)
        data = self.prepare_message(message)
        self.debug('POST data: %s' % pprint.pformat(data))
        try:
            response = client.sms.messages.create(**data)
        except Exception, e:
            self.exception(e)
            return False
        self.info('SENT')
        self.debug(response)
        return True

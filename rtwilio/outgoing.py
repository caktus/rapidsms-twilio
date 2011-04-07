import pprint
import datetime
import twilio

from rapidsms.backends.base import BackendBase


class TwilioBackend(BackendBase):
    """ A RapidSMS backend for Twilio (http://www.twilio.com/) """

    api_version = '2008-08-01'

    def configure(self, config=None, **kwargs):
        super(TwilioBackend, self).configure(**kwargs)
        self.config = config
        self.account = twilio.Account(self.config['account_sid'],
                                      self.config['auth_token'])

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
        except Exception, e:
            self.exception(e)
            return False
        self.info('SENT')
        self.debug(response)
        return True

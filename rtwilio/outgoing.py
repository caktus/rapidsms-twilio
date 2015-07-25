import pprint
import logging

from twilio.rest import TwilioRestClient

from rapidsms.backends.base import BackendBase
from rapidsms.errors import MessageSendingError


logger = logging.getLogger(__name__)


class TwilioBackend(BackendBase):
    """A RapidSMS backend for Twilio (http://www.twilio.com/)."""

    def configure(self, config=None, **kwargs):
        self.config = config
        self.client = TwilioRestClient(self.config['account_sid'],
                                       self.config['auth_token'])

    def prepare_message(self, id_, text, identities, context):
        encoding = self.config.get('encoding', 'ascii')
        encoding_errors = self.config.get('encoding_errors', 'ignore')
        data = {
            'from_': self.config['number'],
            'body': text.encode(encoding, encoding_errors),
        }
        if 'callback' in self.config:
            data['status_callback'] = self.config['callback']
        return data

    def send(self, id_, text, identities, context={}):
        logger.debug('Sending message: %s' % text)
        data = self.prepare_message(id_, text, identities, context)
        failed_identities = []
        for identity in identities:
            data['to'] = identity
            logger.debug('POST data: %s' % pprint.pformat(data))
            try:
                self.client.sms.messages.create(**data)
            except Exception:
                failed_identities.append(identity)
                logger.exception("Failed to create Twilio message.")
        if failed_identities:
            raise MessageSendingError(
                "Messages to some identities failed.",
                failed_identities
            )

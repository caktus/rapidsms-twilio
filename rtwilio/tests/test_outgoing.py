try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from django.test import TestCase

from rapidsms.errors import MessageSendingError
from rapidsms.tests.harness import CreateDataMixin

from rtwilio.outgoing import TwilioBackend


class SendTest(CreateDataMixin, TestCase):

    def test_required_fields(self):
        """Twilio backend requires Gateway URL and credentials."""
        self.assertRaises(TypeError, TwilioBackend, None, "twilio")

    def test_outgoing_keys(self):
        """Outgoing POST data should contain the proper keys."""
        message = self.create_outgoing_message()
        config = {'number': '+12223334444',
                  'account_sid': self.random_string(34),
                  'auth_token': self.random_string(34)}
        backend = TwilioBackend(None, "twilio", config=config)
        data = backend.prepare_message(id_=message.id, text=message.text,
                                       identities=message.connections[0].identity,
                                       context={})
        self.assertTrue('from_' in data)
        self.assertFalse('to' in data)
        self.assertTrue('body' in data)

    def test_outgoing_unicode_characters(self):
        """Ensure outgoing messages are encoded properly."""
        data = {'text': self.random_unicode_string(20)}
        message = self.create_outgoing_message(data=data)
        config = {'number': '+12223334444',
                  'account_sid': self.random_string(34),
                  'auth_token': self.random_string(34),
                  'encoding': 'UTF-8'}
        backend = TwilioBackend(None, "twilio", config=config)
        data = backend.prepare_message(id_=message.id, text=message.text,
                                       identities=message.connections[0].identity,
                                       context={})
        self.assertEqual(data['body'].decode('UTF-8'), message.text)

    @patch('twilio.rest.resources.sms_messages.SmsMessages.create')
    def test_send_calls_twilio_api(self, mock_twilio):
        """Backend.send calls Twilio API."""
        message = self.create_outgoing_message()
        config = {'number': '+12223334444',
                  'account_sid': self.random_string(34),
                  'auth_token': self.random_string(34),
                  'encoding': 'UTF-8'}
        backend = TwilioBackend(None, "twilio", config=config)
        backend.send(message.id, message.text, [message.connections[0].identity])
        mock_twilio.assert_called_with(
            body=message.text.encode('utf-8'),
            from_=config['number'],
            to=message.connections[0].identity
        )

    @patch('twilio.rest.resources.sms_messages.SmsMessages.create')
    def test_send_raises_failures(self, mock_twilio):
        """Backend.send raises any Exceptions, labelling them MessageSendingError."""
        message = self.create_outgoing_message()
        config = {'number': '+12223334444',
                  'account_sid': self.random_string(34),
                  'auth_token': self.random_string(34),
                  'encoding': 'UTF-8'}
        backend = TwilioBackend(None, "twilio", config=config)
        mock_twilio.side_effect = Exception
        with self.assertRaises(MessageSendingError):
            backend.send(message.id, message.text, [message.connections[0].identity])

    @patch('twilio.rest.resources.sms_messages.SmsMessages.create')
    def test_send_can_specify_failed_identities(self, mock_twilio):
        """Backend.send can specifiy individual failures."""
        config = {'number': '+12223334444',
                  'account_sid': self.random_string(34),
                  'auth_token': self.random_string(34),
                  'encoding': 'UTF-8'}
        backend = TwilioBackend(None, "twilio", config=config)
        # first identity raises an exception, second one doesn't
        mock_twilio.side_effect = [Exception, None]
        with self.assertRaises(MessageSendingError) as cm:
            backend.send(id_=self.random_string(), text=self.random_string(),
                         identities=['boom', 'success'])
        if hasattr(cm.exception, 'failed_identities'):
            failed_identities = cm.exception.failed_identities
        else:
            failed_identities = cm.exception.args[1]
        self.assertIn('boom', failed_identities)
        self.assertNotIn('success', failed_identities)

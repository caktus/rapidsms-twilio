from django.test import TestCase

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

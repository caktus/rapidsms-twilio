from django.test import TestCase
from django.core.urlresolvers import reverse

from rapidsms.tests.harness import RapidTest, CreateDataMixin

from rtwilio.forms import TwilioForm
from rtwilio.outgoing import TwilioBackend


class TwilioFormTest(CreateDataMixin, TestCase):

    def test_valid_form(self):
        """Form should be valid if GET keys match configuration."""
        data = {"From": "+12223334444",
                "To": "+19998887777",
                "Body": self.random_string(50),
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        form = TwilioForm(data, backend_name='rtwilio-backend')
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Form is invalid if POST keys don't match configuration."""
        data = {'invalid-phone': '1112223333', 'invalid-message': 'hi there'}
        form = TwilioForm(data, backend_name='rtwilio-backend')
        self.assertFalse(form.is_valid())

    def test_get_incoming_data(self):
        """get_incoming_data should return matching text and connection."""
        data = {"From": "+12223334444",
                "To": "+19998887777",
                "Body": self.random_string(50),
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        form = TwilioForm(data, backend_name='rtwilio-backend')
        form.is_valid()
        incoming_data = form.get_incoming_data()
        self.assertEqual(data['Body'], incoming_data['text'])
        self.assertEqual(data['From'],
                         incoming_data['connection'].identity)
        self.assertEqual(data['SmsSid'],
                         incoming_data['fields']['external_id'])
        self.assertEqual('rtwilio-backend',
                         incoming_data['connection'].backend.name)


class TwilioViewTest(RapidTest):

    urls = 'rtwilio.tests.urls'
    disable_phases = True

    def test_invalid_response(self):
        """HTTP 400 should return if data is invalid."""
        data = {'invalid-phone': '1112223333', 'message': 'hi there'}
        response = self.client.post(reverse('rtwilio-backend'), data)
        self.assertEqual(response.status_code, 400)

    def test_get_disabled(self):
        """HTTP 405 should return if GET is used."""
        data = {"From": "+12223334444",
                "To": "+19998887777",
                "Body": self.random_string(50),
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        response = self.client.get(reverse('rtwilio-backend'), data)
        self.assertEqual(response.status_code, 405)

    def test_valid_post_message(self):
        """Valid POSTs should pass message object to router."""
        data = {"From": "transport",
                "To": "+14155554345",
                "Body": "foo",
                "AccountSid": self.random_string(34),
                "SmsSid": self.random_string(34)}
        response = self.client.post(reverse('rtwilio-backend'), data)
        self.assertEqual(response.status_code, 200)
        message = self.inbound[0]
        self.assertEqual(data['Body'], message.text)
        self.assertEqual(message.fields['external_id'], data['SmsSid'])
        self.assertEqual('rtwilio-backend', message.connection.backend.name)


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
